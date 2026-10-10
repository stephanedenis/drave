# Sprint « cerveau complet » — état d'avancement

> Lancé le 9 octobre à 17 h, **en autonomie jusqu'au 10 octobre 9 h (HAE)**.
> Plan de référence : `docs/plan-cerveau-complet.md` § 4 (premier sprint).
> Ce fichier est mis à jour **à chaque round** : il est la mémoire du sprint.

---

## C6/C2 — FAIT (10 octobre 18 h) : LA MÉMOIRE QUI SERT, de bout en bout

`--episodique-extraire F` ferme la chaîne : indexer → **retrouver par le contenu** →
**injecter** l'état retrouvé dans un calcul qui n'a pas vécu l'épisode. L'état écrit est
l'état VÉCU (la moyenne est rajoutée si le magasin est décorrélé).

Magasin de 1 750 états de l'invite A (code au jeton 740), indice extérieur (l'invite B,
même texte SANS le code) :

| étape | mesure |
|---|---|
| rappel | épisode 437 · recouvrement 25/64 · **303 jetons** de l'aiguille (hasard 448) |
| injection α = 0 | `150px` — témoin de non-effet |
| **injection α = 0,2 / 1** | **`The vault access code is`** |
| injection α = 5 | `"150px` (saturé) |

**La chaîne fonctionne** : le modèle DIT la phrase-cadre de l'aiguille alors que ni le
code ni cette phrase ne sont dans son contexte. **Mais le code n'est pas produit** — et
la cause est en haut du tableau : l'épisode retrouvé est à **303 jetons** de l'aiguille,
donc son préfixe ne contient pas encore le code.

**⇒ LE GOULOT EST LE RAPPEL, PAS LA GREFFE.** C'est la conclusion utile du round : la
greffe est un mécanisme qui marche (corrigée et vérifiée), et ce qui limite l'usage est la
qualité du rappel par un indice purement sémantique (1,5× le hasard).

**Réserves écrites** : l'état stocké est la sortie **normalisée** (norme 306) alors que la
greffe injecte un résidu brut (54-66) — l'échelle est absorbée par la normalisation
finale, mais stocker le résidu serait plus cohérent ; un seul indice, un seul texte.

---

## C6 — FAIT (10 octobre 19 h 30) : le rappel dépend de l'INDICE (8 indices mesurés)

Huit indices prélevés dans l'invite B (positions depuis la fin : 1, 2, 4, 8, 16, 32, 64,
128), chacun servant de requête au magasin de A (aiguille au jeton 740, hasard 448) :

| indice | épisode | distance |
|---|---|---|
| 4ᵉ depuis la fin | 690 | **50** |
| 2ᵉ | 429 | 311 |
| 32ᵉ | 437 | 303 |
| dernière | 437 | 303 |
| 16ᵉ | 393 | 347 |
| 64ᵉ | 393 | 347 |
| 128ᵉ | 1630 | 890 |
| 8ᵉ | 1743 | 1 003 |

**Moyenne 444 · médiane 329 · meilleure 50 · pire 1 003 · hasard 448.**

1. **un indice existe qui trouve l'aiguille** : 50 jetons, **9× mieux que le hasard** ;
2. **mais UN SEUL sur huit** : les autres sont au niveau du hasard. Le « 3,3× mieux que le
   hasard » du round 2 était donc **un tirage chanceux** — et sa fragilité (136 puis 378
   selon un point d'interrogation) s'explique ainsi ;
3. **la limite est le CHOIX DE L'INDICE, pas la mémoire** — et ce choix ne se devine pas :
   rien ne désigne la 4ᵉ position depuis la fin plutôt que la dernière.

**Suite — six dernières positions prélevées une à une : le rappel n'est PAS continu.**
`:` 303 · `Answer` 311 · `.` 533 · **`only` 50** · **`code` 1 006** · `the` 1 005.

**Deux jetons VOISINS — « code » et « only » — donnent 1 006 et 50 jetons.** Rien de
lexical ne l'explique : les deux états ont lu presque le même texte. C'est que la clé est
un **k-WTA** (64 canaux sur 16 384) : une petite variation de l'état fait entrer et sortir
des canaux, donc la clé **saute**. Il n'y a aucune pente à suivre pour s'approcher du bon
indice — voilà pourquoi il est impossible à deviner, et c'est un **mécanisme**, pas une
fatalité.

**Trois voies, aucune mesurée** : rendre la clé **stable** en la formant sur une FENÊTRE de
positions (union/intersection des k-WTA voisins) ; interroger avec plusieurs indices et
garder le meilleur (le recouvrement ne les départage pas : le gagnant n'a que 25/64) ;
ou abandonner le rappel sémantique et faire entrer le contenu comme JETONS.
**Nouveau** : `--etat-fin` accepte une liste de positions (1,2,4,8…) — huit indices en un
seul parcours, au lieu de huit parcours de 70 s.

---

## C6 — FAIT (10 octobre 22 h) : clé de FENÊTRE — prédiction RÉFUTÉE

Le §30 avait identifié le mécanisme (la clé est un k-WTA, donc elle saute d'un jeton à
l'autre). Prédiction falsifiable : **former la clé sur la moyenne de W positions voisines
doit lisser l'hypersensibilité**. Mesuré (`--episodique-fenetre`) :

| fenêtre | indice « only » (le bon) | indice « code » (le mauvais) | séparation |
|---|---|---|---|
| **1** | **50** | 1 006 | **1,31/64** |
| 4 | 653 | 1 005 | 1,73/64 |
| 16 | 573 | 1 004 | 4,58/64 |
| 64 | **449** (= hasard) | 1 004 | **19,94/64** |

**Réfutée** : le lissage ne réduit pas l'hypersensibilité, il **détruit le bon indice**
(50 → 449, le hasard) et **effondre la séparation** (1,31 → 19,94 canaux partagés).

**Troisième voie indépendante qui confirme le §24 quater** : abstraire par moyennage
détruit la rappelabilité (prototype moyen 22 % contre 87 % pour l'exemplaire ; clé moyenne
qui ne retrouve pas le passage ; fenêtre moyenne qui fait tomber le meilleur indice au
hasard). **La sélectivité de cette mémoire EST la netteté de sa clé** — et
l'hypersensibilité à l'indice en est le prix.

**Conséquence, et elle change de direction** : le lissage étant exclu et le choix de
l'indice n'étant pas devinable, **retrouver un passage depuis une question n'est pas ce
que le rappel par le contenu sait faire**. Ce qui reste solide : la complétion de motif
(Δ = 2 jetons à 50 % de dégradation), la localisation, et l'injection d'un état retrouvé.
Pour la recherche par question : des **jetons** (RAG) ou une **clé apprise**.

---

## C10 — FAIT (10 octobre 23 h) : budget d'octets par lien, déclaré et vérifié

Le plan demandait des budgets vérifiés au démarrage ; la mesure a corrigé le plan : **la
taille d'un flux dépend de l'ACTIVITÉ, pas du mode** (1 951 octets à 97,7 % d'activité,
1 096 à 50 %). Le budget se compare donc à **ce qui passe**, au pas où il passe.

Topologie : `"budget_octets": N` sur un lien. Porte `tools/porte-budget.sh` :

| cas | mesure |
|---|---|
| aucun budget | 111,9225 · 1 951 octets/pas · code 0 |
| budget généreux (2 451) | **111,9225 — identique** · code 0 |
| budget insuffisant (975) | premier flux **1 860 octets** ⇒ arrêt **au pas 0**, message nommant lien/octets/budget/pas, **code 6**, **aucune perplexité rendue** |

Même règle que C4 et C9 : **s'arrêter et le dire**, jamais rendre un chiffre qui mentirait
sur ses conditions.

---

## C10 (suite) — FAIT (11 octobre 1 h 30) : budget de LATENCE par lien

Troisième volet des budgets du plan (`{paires/s, octets/s, ms}`), après les octets. Déclaré
par `"budget_ms": N`, comparé à l'**allé-retour mesuré** de chaque pas.

| cas | mesure |
|---|---|
| latence généreuse (100 000 ms) | 111,9225 — **identique** · code 0 |
| latence insuffisante (1 ms) | `LATENCE DÉPASSÉE : **20,1 ms pour un budget de 1 ms, au pas 0**` · **code 8** · aucune perplexité |

**Quatre codes d'arrêt distincts** : **5** = borne de pas (C4) · **6** = budget d'octets ·
**7** = panne de lien (C11) · **8** = budget de latence. Un script nomme la cause sans lire
les messages.

**Défaut de porte attrapé** : la porte écrasait la variable `D` (le binaire) avec la sortie
du pilote — le cas suivant échouait en **127** (« command not found »), ce qui ne disait
rien de ce qu'on mesurait.

---

## C11 — FAIT (11 octobre 0 h 30) : pannes de lien nommées, code distinct, sans résultat partiel

Le plan prévoyait un `best-effort` qui « saute la région et annonce l'écart ». **La mesure
oblige à refuser cette sémantique** : sauter douze couches ne calcule pas une version
approchée, cela calcule **un autre modèle**. Conduite retenue : **s'arrêter en disant tout**.

`tools/porte-pannes.sh` (3 cas, verte) :

| cas | mesure |
|---|---|
| nominal | 33,0156 · code 0 |
| **pair tué en cours de route** | `PANNE sur le lien local → d … s'arrête au pas 12 (43 968 octets échangés)` · **code 7** · aucune perplexité |
| **pair absent** | `INJOIGNABLE (Connection refused)` · **code 7** en **2 s** · aucune perplexité |

Codes distincts : **5** = borne de pas (C4) · **6** = budget (C10) · **7** = panne (C11).

**Deux défauts trouvés** : un pair absent faisait **paniquer** le pilote (`expect` sur la
connexion, code 134) — corrigé en panne nommée ; et la porte attendait un événement fragile
(`client connecté`) au lieu de juger sur le code et le message.

**Reste non fait** : la REPRISE — un pair qui revient a perdu son cache KV, donc continuer
serait faux ; reprendre demanderait de rejouer le préfixe (checkpoint/restart).

---

## BALAYAGE DES PORTES — FAIT (11 octobre 6 h 30) : le piège de fenêtre était latent ailleurs

Après avoir corrigé `porte-reparti-moteur` (§ précédent), balayage des 20 portes : **deux**
seulement comparent un entier à un réparti. L'une affirmait l'égalité (corrigée), l'autre
**`porte-topologie`** imprimait les deux perplexités **côte à côte** sans les comparer — avec
le même écart de fenêtre : son fichier a **255** jetons et sa limite en annonçait **128**,
donc la référence portait sur les **premiers** 128 jetons et le découpage sur les **derniers**.
Elle passait, mais **invitait à une comparaison fausse**.

Corrigé (jetons comptés) : **référence 5,3719 · découpage 5,3719 · écart de flux 0,00e0**.

**Règle écrite une fois pour toutes** : dans une porte, `--limit` doit valoir **le nombre de
jetons du fichier, compté et non écrit à la main**, dès qu'un chemin réparti intervient. Les
deux portes qui le faisaient à la main s'étaient trompées toutes les deux. Les onze autres
sont saines par construction (réparti contre réparti, ou « référence locale » du même run).

---

## C11 (découverte) — FAIT (11 octobre 5 h 30) : le registre des régions

Une topologie qui écrit une adresse décrit UN déploiement ; la même sur trois machines en
demanderait trois. `--registre FICHIER` (lignes `region hote:port`) résout les instances
**nommées**, des deux côtés (pilote et nœud relais). Une instance qui contient déjà `:` n'est
pas touchée : les topologies existantes marchent au caractère près.

`tools/porte-registre.sh`, 3 cas verts :

| cas | mesure |
|---|---|
| topologie **nommée** + registre | **113,0068** · code 0 |
| même topologie, **adresse en dur** | **113,0068 — identique** |
| région **absente** du registre | refus **en la nommant**, code 2, rien n'est calculé |

**Défaut trouvé en écrivant la porte** : le contrôle de cohérence comparait `--ppl-reparti`
à l'instance **brute** — une topologie nommée était refusée (code 3) comme contradictoire
alors que les deux sources disaient la même chose. **La résolution doit précéder le
contrôle** ; c'est écrit dans le code à cet endroit.

---

## LA ROUGE DE RÉPARTITION — INSTRUITE ET CORRIGÉE (11 octobre 4 h 30) : c'était la PORTE

Hypothèses éliminées par la mesure : le **routage** (la variante dense échoue aussi, 37,8 %),
le **transport** (flux à 0,00e0), et « notre modèle n'est pas découpable » (contredit
ci-dessous).

**La cause** : le fichier d'identifiants contient **255 jetons**, la porte en annonçait 128 —
et les deux chemins fenêtrent **différemment** : `--ppl` note les `limit` **premiers** jetons,
`--ppl-reparti` **tronque aux `limit` derniers** (« 256 jetons fournis > limite 128 : troncature
aux 128 derniers »). La porte comparait **deux textes différents**.

**Après correction** (le nombre de jetons est compté, plus supposé) :

| modèle | entier | réparti | écart |
|---|---|---|---|
| `moteur_dense.gguf` | 173,0196 | **173,0196** | **0,0000 %** |
| `moteur_route.gguf` | 173,0196 | **173,0196** | **0,0000 %** |

**PORTE TENUE** : notre modèle entraîné (Qwen3-MoE) **survit au découpage au chiffre près**,
routage compris — ce que la rouge laissait croire faux depuis deux jours. **20 portes vertes
sur 20**, 122 tests.

**Asymétrie de protocole à retenir** : `--limit` = « les N premiers » en perplexité, « les N
derniers » en réparti.

---

## VÉRIFICATION COMPLÈTE — FAITE (11 octobre 3 h) : 19 portes vertes, 1 rouge nommée

Suite complète des portes (`tools/porte-*.sh`, 20 fichiers) **après les huit rounds** qui ont
touché le chemin d'exécution (fusion d'état, pont, budget, pannes, capture d'état) :

**19 vertes · 1 rouge · 122 tests verts.**

Vertes : budget · bus · bus-socket · coupe · delais · episodique · flux · fusion · greffe ·
horloge · indice · melange · mistral · pannes · pont · reflexe · tokenizer-kimi · topologie ·
trace.

**La rouge : `porte-reparti-moteur`** — perplexité entière **321,9623** contre répartie
**132,8349** (écart 58,7 %) alors que **l'écart de flux est 0,00e0**. C'est la porte de NOTRE
modèle (`/tmp/moteur_route.gguf`, entraîné ici), avec `COUCHES=2` : deux couches locales, le
reste à distance.

**Ce que je peux affirmer et ce que je ne peux pas** : les huit rounds n'ont ajouté que des
chemins INACTIFS par défaut sur cette porte (fusion sans `--fusion-etat`, pont sans
`--pont-k`, budget sans `budget_octets`/`budget_ms`, pannes seulement en cas d'erreur,
capture sans `--etat-sortie`, borne sans `--pas-max`) — donc **aucun de ces changements ne
peut produire un écart de 58 %**. Mais je n'ai pas remonté au commit d'avant le sprint pour
le prouver, et je ne l'affirme donc pas : **c'est une rouge PRÉ-EXISTANTE, non expliquée**, et
elle est écrite comme telle.

**Prochaine action sur ce point** : déterminer si la cause est le MODÈLE (un modèle entraîné
ici dont le découpage change réellement le calcul — routage d'experts, normes) ou la PORTE
(un fichier `/tmp/moteur_route.gguf` périmé par rapport à l'entraîneur actuel). La commande :
régénérer `/tmp/moteur_route.gguf` et `/tmp/route_ids.txt` avec `tools/entrainer_moteur.py`,
puis rejouer `tools/porte-reparti-moteur.sh` ; et si la rouge persiste, comparer les logits
entier/réparti position par position (l'outil existe : `compare_logits.py`).

---

## E4 — FAIT (11 octobre 7 h 30) : l'équilibre excitation/inhibition, mesuré

Levier existant `--ffn-gain couche:valeur`. Référence (sans réglage) **14,6496**, Qwen2.5-0.5B,
128 jetons. Porte `tools/porte-gain.sh`, 4 cas verts.

1. **INVARIANT** : `--ffn-gain L:1.0` **EST** l'absence de réglage — 14,6496 sur les couches
   0, 6 et 18. Sans lui, aucune autre ligne ne comparerait quoi que ce soit.
2. **INHIBITION** : la courbe est **MONOTONE** (couche 12 : 15,69 · 16,30 · 17,12 · 19,48)
   ⇒ l'hypothèse « un peu d'inhibition fait du bien » est **RÉFUTÉE** de ce côté.
3. **AMPLIFICATION** : l'optimum est **INTÉRIEUR** et net sur les premières couches —
   couche 0 à **0,75 → 12,9635** (**−11,5 %**), couche 1 à 0,5 → 13,7907 (−5,9 %), couche 2
   sans optimum utile.
4. **FALAISE** : couche 0 à 0,25 → **996,04** (**68× pire**) : un gain trop faible à la
   première couche ne dégrade pas un peu, il **casse** le modèle.

5. **Le profil complet sur les 24 couches à 0,75 LOCALISE l'effet** : couches 0 et 1
   gagnent (−11,5 % et −4,5 %), couches 2 et 3 **perdent beaucoup** (+9,2 %, +10,6 %),
   couches 4-16 sont **neutres** (±1 %), seules 17, 21, 23 repassent au-dessus de +3 %.
   Le déséquilibre n'est donc **pas réparti : il est à l'ENTRÉE**. Un **profil appris par
   couche** reste un levier mesuré (−11,5 % sans rien entraîner) — piste directe pour le
   dessin I de `docs/modele-pour-drave.md` — mais il porte sur deux couches, pas sur
   vingt-quatre.

---

## E4 (suite) — FAIT (11 octobre 9 h) : les gains NE SE COMPOSENT PAS

`--ffn-gain` accepte désormais une **liste** (`L:V,L:V`) : la question « les gains se
composent-ils ? » devient mesurable. Référence 14,6496.

| profil | perplexité | écart |
|---|---|---|
| **`0:0.75` seul** | **12,9635** | **−11,51 %** |
| `1:0.5` seul | 13,7907 | −5,86 % |
| `0:0.75,1:0.5` | 13,7679 | −6,02 % |
| `0:0.9,1:0.6` | 13,4209 | −8,39 % |
| `0:0.75,1:0.5,2:1.0` | 13,7679 | **identique** (1,0 est neutre) |

**Ajouter le gain de la couche 1 DÉGRADE celui de la couche 0** : les deux réglages
s'antagonisent. Le meilleur profil mesuré est **un réglage SEUL**. Et un gain de 1,0 dans un
profil est **exactement neutre** — l'identité tient aussi à l'intérieur d'un profil.

**Conséquence pour le dessin I, plus dure que celle du round précédent** : non seulement le
profil n'a que deux couches utiles, mais **le composer empire les choses**. Un profil appris
aurait à découvrir que la réponse est « une seule couche, un seul gain » — ce qu'un gradient
sur peu de paramètres peut très bien ne pas trouver, puisqu'il optimiserait les deux ensemble.

**Porte `porte-gain.sh` : 6 cas verts.**

---

## AUDIT DES DRAPEAUX PAR CHEMIN — FAIT (11 octobre 11 h) : méthode, portée, et ce qui reste

Après le défaut de câblage de `--ffn-gain`, criblage statique des trois fonctions d'exécution
(assignations `mdl.<champ> = …`) : `run_infer` 30 champs, `run_ppl` 16, **`run_ppl_reparti` 3**.

**L'ANGLE MORT, et il est important** : le criblage annonce 29 champs « absents » pour
`run_infer`, dont `act_thresh`, `act_topk`, `attn_topk`, `qk_topk`, `moe_topk` — **qui sont
câblés**, mais par le **helper** `appliquer_quantification`, que le criblage ne lit pas. Il ne
voit que les assignations écrites *dans* la fonction. Conclusion : **« absent du criblage »
n'est pas « non câblé »**, et le confondre aurait produit un faux rapport.

**Ce qu'il a établi** : le chemin réparti assigne 3 champs en propre, le helper en couvre 7 de
plus, et c'est **ce qui restait hors des deux** qui contenait le défaut (`ffn_gain`) — la
méthode a donc servi, avec sa portée exacte.

**Les candidats ont été INSTRUITS (round suivant), et la mesure vide était MON erreur** : le
port du banc montait à 65 949, **au-delà de 65 535** — le nœud ne se liait pas, et le moteur le
disait (`INJOIGNABLE (invalid port value)`). Reprise avec un port valide et `--options-strict` :

| drapeau | réparti | verdict |
|---|---|---|
| `--act-topk 64` | 1 137 878,95 | **agit** |
| `--qk-topk 64` | 24 955,44 | **agit** |
| `--act-thresh 0,01` | 209,7804 | **agit** |
| **`--attn-window 16`** | 180,5245 | **SANS EFFET** (ne voyage pas dans `Act`) |
| **`--attn-topk 64`** | 180,5245 | **SANS EFFET** (voyage pourtant : champ présent dans `Act`) |
| `--moe-topk 2` | 180,5245 | normal — **Qwen2.5-0.5B est dense**, sans experts |

**Instruits à contexte long (512 jetons) :**

- **`--attn-topk` : PAS de défaut** — sans effet à 32 jetons (180,5245), il **agit** à 512
  (18,5520 → **18,4032**). Mon hypothèse était la bonne : à contexte court, l'attention est
  déjà triviale ;
- **`--attn-window` : un vrai trou, et une correction REVERTÉE.** À 512 jetons il **agit en
  local** (13,1368 → **21,5801**) et **pas en réparti** (18,5520) ⇒ il n'est câblé que dans
  `run_infer` et `run_ppl` (même famille que `--ffn-gain`). Et il **ne voyage pas** dans la
  trame (`Act` ne porte ni `attn_window`, ni `swa_pattern`, ni `attn_sinks`). Le câblage a été
  tenté : il rend un **résultat VIDE**, cause non diagnostiquée ⇒ **REVERTÉ** plutôt que laissé
  dans l'arbre — une régression silencieuse vaut moins qu'un manque écrit. Après revert :
  référence répartie **18,5520**, 122 tests verts, arbre propre.

**INSTRUIT ET RÉSOLU PAR UN REFUS.** Le câblage refait — **en regardant la sortie complète**,
comme la commande du round précédent le demandait — ne rend plus un vide mais un résultat
**FAUX ET SILENCIEUX**, ce qui est pire : le pilote applique la fenêtre à ses douze couches, le
nœud garde la sienne.

| avec `--attn-window 64` câblé | perplexité |
|---|---|
| référence locale (12 couches du pilote) | **195,5685** |
| découpage (12 + 12) | **50,3829** |
| écart de flux | **7,42e-1** |

**La correction est donc devenue un REFUS EXPLICITE** : en réparti, si `--attn-window`,
`--swa-pattern` ou `--attn-sinks` est donné, le moteur s'arrête en expliquant (**code 2**,
aucune perplexité). Un drapeau inerte est un défaut ; **un drapeau qui fait calculer deux
modèles différents sous le même nom en est un pire**. Ces réglages restent honorés en local et
en inférence, où ils sont mesurés (13,1368 → 21,5801).

**Reste à faire pour les honorer en réparti** : les ajouter à `struct Act` et à l'encodeur de
trame (**protocole v7**), puis les appliquer côté nœud.

**`porte-gain.sh` : 9 cas verts.**

---

## DÉFAUT TROUVÉ ET CORRIGÉ (11 octobre 10 h 30) : `--ffn-gain` ne faisait RIEN en réparti

En mesurant l'interaction du gain d'entrée avec le découpage, la mesure a rendu **le même
chiffre avec et sans le drapeau** (42,5477). Ce n'était pas une absence d'effet : une absence
de **câblage** — `--ffn-gain` était appliqué dans `run_infer` et `run_ppl`, **pas** dans
`run_ppl_reparti`. Dans le chemin réparti, le réglage ne faisait rien, **en silence**.

C'est la famille de défauts que ce dépôt traque, et il comptait double : un réglage fin qui ne
survit pas à la distribution est ce qu'on ne veut pas découvrir en production.

**Corrigé** et mesuré : réparti sans réglage **180,5245**, avec `0:0.75` **222,3496** ⇒ le
drapeau agit. Le SIGNE n'est pas celui du chemin local (−11,5 % sur 128 jetons) parce que la
fenêtre de 32 jetons est trop courte : **ce n'est pas une mesure de qualité, c'est un contrôle
de câblage**, et la porte le traite comme tel (elle exige que les chiffres **diffèrent**).

**Et le piège de fenêtre a mordu une troisième fois** dans la même tentative : `--ppl --limit
128` note les **128 premiers** jetons d'un fichier qui en compte 85 625, `--ppl-reparti`
**tronque aux 128 derniers**. Trois portes le documentent maintenant.

**`porte-gain.sh` : 8 cas verts.**

---

## E4 (suite) — FAIT (11 octobre 10 h) : généralisation et conditions

Deux axes, même conclusion : **la direction tient, la magnitude dépend des conditions**.

| axe | mesure |
|---|---|
| autre **quantification** (Q4_0) | 0,75 à la couche 0 → **14,7453** contre **15,8055** = **−6,7 %** (Q8_0 : −11,5 %) |
| autre **fenêtre** (256 jetons) | **17,1915** contre **17,4315** = **−1,4 %** (128 jetons : −11,5 %) |

⇒ le gain d'entrée n'est **pas un artefact de quantification** (−6,7 % sur Q4_0), mais **il
décroît fortement avec la fenêtre** : −11,5 % est un **point de mesure**, pas une propriété du
modèle. **La porte exige que la magnitude décroisse** — un futur relecteur ne pourra donc pas
citer le meilleur chiffre sans voir la condition.

**`porte-gain.sh` : 7 cas verts.**

---

## VÉRIFICATION DU CHANGEMENT DE TYPE `ffn_gain` — FAITE (11 octobre 9 h 30)

Le drapeau est passé de `Option<(usize, f32)>` à `Option<Vec<(usize, f32)>>` (profil de gains),
ce qui touche le chemin d'exécution du moteur. Vérifié :

- **`porte-flux.sh` : 5 modes verts, code 0** — le changement est INACTIF par défaut, et les
  cinq modes du protocole (0 à 4) donnent exactement les mêmes écarts qu'avant (0,00e0 ·
  0,00e0 · 3,65e-2 · 0,00e0 · 4,45e-3) ;
- **la référence de perplexité est inchangée** : 14,6496 sur le jeu d'essai, identique à la
  mesure du round précédent ;
- **`porte-gain.sh` : 6 cas verts**, y compris l'identité (`L:1.0` = absence de réglage) qui
  est la garde du nouveau format ;
- **122 tests verts**.

C'est la règle de l'objectif appliquée à la lettre : « `porte-flux.sh` après toute modification
du chemin d'exécution ».

---

## VÉRIFICATION APRÈS LE REFUS DES RÉGLAGES NON TRANSPORTABLES — FAITE (11 octobre 12 h 30)

Le refus ajouté (§ précédent) est un **changement du chemin d'exécution réparti** : la règle de
l'objectif s'applique donc à la lettre (« `porte-flux.sh` après toute modification du chemin
d'exécution »). Vérifié :

| porte | résultat |
|---|---|
| **`porte-flux.sh`** | **code 0** — les cinq modes du protocole sont inchangés : 0,00e0 · 0,00e0 · 3,65e-2 · 0,00e0 · 4,45e-3 |
| **`porte-pannes.sh`** | **code 0** — les pannes restent nommées (lien, pas, octets), code 7, aucune perplexité |
| **`porte-registre.sh`** | **code 0** — registre et adresse en dur donnent le même résultat |
| **`porte-gain.sh`** | **9 cas verts**, dont le refus lui-même |
| **tests** | **122 verts** |

Le refus ne se déclenche que si l'un des trois réglages est **demandé** : une exécution qui ne
les demande pas suit exactement le chemin d'avant.

---

## PROTOCOLE v7 — SPÉCIFIÉ À L'OCTET PRÈS (11 octobre 13 h), PAS ENCORE IMPLÉMENTÉ

Le refus du round précédent (`--attn-window`, `--swa-pattern`, `--attn-sinks` non transportables)
se lève en faisant voyager ces trois réglages. **Reconnaissance faite** : l'en-tête de trame est
**plein**.

```text
offsets actuels (TAILLE_TETE = 79 octets, aucune marge) :
  0   magie u32        4   version u8     5   mode u8
  6   debut u32       10   fin u32       14   pos u32       18   n u32
 22   echelle f32     26   levels f32    30   thresh f32    34   topk u32
 38   renorm u8       39   topk_proj[7] u32 (39..67)
 67   attn_topk u32   71   qk_topk u32   75   moe_topk u32
```

**Les cinq modifications, et rien d'autre :**

1. `struct Act` : trois champs `attn_window: u32`, `swa_pattern: u32`, `attn_sinks: u32` (+ les
   remplir dans `du_modele`, + les appliquer dans `appliquer`) ;
2. `TAILLE_TETE` : `79 + 12` = **91** octets ;
3. `VERSION_FLUX` : **6 → 7** (le décodeur refuse une version étrangère — et c'est voulu : deux
   binaires de versions différentes ne doivent pas se parler à moitié) ;
4. `tete_flux` : trois `extend_from_slice` de plus, aux offsets **79, 83, 87** ;
5. `recevoir_flux` : trois lectures `u(79)`, `u(83)`, `u(87)` — puis **retirer le refus**.

**Ce qui vérifie ce changement** : `porte-flux.sh` fait parler LES DEUX côtés sur les cinq modes
du protocole et compare les écarts à 0,00e0 / 0,00e0 / 3,65e-2 / 0,00e0 / 4,45e-3 — un en-tête
décalé d'un octet y échoue immédiatement. C'est le garde-fou qui rend ce changement tentable, et
il existe déjà.

**Pourquoi ce n'est pas fait dans ce round** : l'en-tête est PLEIN, donc la modification touche
l'encodeur ET le décodeur ET la version — trois endroits où une erreur d'un octet casse les cinq
modes à la fois. Le round qui l'entreprend doit avoir de la marge pour déboguer ; celui-ci a
préféré **spécifier à l'octet près** plutôt que de laisser un arbre cassé.

---

## PROTOCOLE v7 — LIVRÉ (11 octobre 15 h 30) : la fenêtre voyage, le refus disparaît

Le round précédent avait reverté le v7 parce que **neuf tests** tombaient. La cause était
précise : les constructeurs de **trame forgée** remplissaient l'en-tête avec **dix mots
littéraux**. Corrigé d'abord — ils **calculent** maintenant le remplissage à partir de
`TAILLE_TETE` — puis le v7 a été appliqué en **11 sites** et tout est vert.

**Mesure, avec `--attn-window 64` en réparti :**

| | perplexité |
|---|---|
| référence locale du run réparti | **18,5520** |
| découpage (12 + 12) | **18,5520** |
| **écart de flux** | **0,00e0** |

Là où le câblage sans transport donnait **195,5685 contre 50,3829** (facteur 4, deux modèles
différents sous le même nom), les deux moitiés appliquent désormais **la même fenêtre**. Le
chemin purement local donne 21,5801 avec le même réglage : un autre calcul, mais un calcul
**annoncé**.

**Le refus est retiré** — il était la bonne conduite tant que la trame ne transportait pas ces
réglages ; il devient un obstacle dès qu'elle les transporte.

**Vérifications** : `porte-flux.sh` **vert**, cinq modes, écarts inchangés (0,00e0 · 0,00e0 ·
3,65e-2 · 0,00e0 · 4,45e-3) — c'est le garde-fou qui aurait attrapé un en-tête décalé d'un
octet ; **122 tests verts**. Enseigné au passage : une modification de protocole se compte en
**trois** endroits — encodeur, décodeur, **et les tests qui le forgent**.

---

## PROTOCOLE v7 — LIVRÉ (11 octobre 15 h 30) : la fenêtre voyage, le refus disparaît

Le round précédent avait reverté le v7 parce que **neuf tests** tombaient. La cause était
précise : les constructeurs de **trame forgée** remplissaient l'en-tête avec **dix mots
littéraux**. Corrigé d'abord — ils **calculent** maintenant le remplissage à partir de
`TAILLE_TETE` — puis le v7 a été appliqué en **11 sites** et tout est vert.

**Mesure, avec `--attn-window 64` en réparti :**

| | perplexité |
|---|---|
| référence locale du run réparti | **18,5520** |
| découpage (12 + 12) | **18,5520** |
| **écart de flux** | **0,00e0** |

Là où le câblage sans transport donnait **195,5685 contre 50,3829** (facteur 4, deux modèles
différents sous le même nom), les deux moitiés appliquent désormais **la même fenêtre**. Le
chemin purement local donne 21,5801 avec le même réglage : un autre calcul, mais un calcul
**annoncé**.

**Le refus est retiré** — il était la bonne conduite tant que la trame ne transportait pas ces
réglages ; il devient un obstacle dès qu'elle les transporte.

**Vérifications** : `porte-flux.sh` **vert**, cinq modes, écarts inchangés (0,00e0 · 0,00e0 ·
3,65e-2 · 0,00e0 · 4,45e-3) — c'est le garde-fou qui aurait attrapé un en-tête décalé d'un
octet ; **122 tests verts**. Enseigné au passage : une modification de protocole se compte en
**trois** endroits — encodeur, décodeur, **et les tests qui le forgent**.

---

## PROTOCOLE v7 — TENTÉ (11 octobre 14 h), REVERTÉ : neuf tests encodent la mise en page v6

Les huit modifications de la spécification du round précédent ont été appliquées — `struct Act`
(3 champs), `du_modele`, `appliquer`, `TAILLE_TETE` (79 → **91**), `VERSION_FLUX` (6 → **7**),
l'encodeur (offsets 79/83/87), le décodeur (`u(79)`, `u(83)`, `u(87)`), et le **retrait du
refus**. Le binaire **compile**, et `cargo build` ne dit rien.

**Mais 9 tests tombent**, et ce sont exactement ceux qui encodent la mise en page v6 :

| test | ce qu'il fixe |
|---|---|
| `entete_et_version_sont_ce_que_les_numeros_disent` | `assert_eq!(TAILLE_TETE, 79, …)` — et la version en commentaire (« 4 quand les top-k sont entrés, 5 quand le mode 4 est apparu, 6 quand… ») |
| les tests de **trame forgée** (`mode4_prefixe_incoherent_est_refuse`, `un_lot_dement_grand_est_refuse_avant_allocation`, …) | ils construisent une trame **à la main**, avec les offsets et la taille de la v6 |

**La modification a donc été REVERTÉE**, et la contrainte de l'objectif est intacte : **122 tests
verts**, arbre propre, porte-flux inchangée. Le round de conception du v7 reste valable — il ne
manquait que ceci, et c'est maintenant écrit :

1. `assert_eq!(TAILLE_TETE, 79, …)` → **91**, et le commentaire de version gagne « 7 quand la
   fenêtre d'attention et le motif glissant sont entrés dans le contrat » ;
2. les constructeurs de **trame forgée** prennent la nouvelle taille — ils liront `TAILLE_TETE`
   plutôt qu'un littéral, sinon le prochain ajout de champ les cassera de la même façon ;
3. **puis** retirer le refus.

**Leçon, et elle est la même que partout dans ce sprint** : le contrat d'échange n'est pas
seulement dans l'encodeur et le décodeur, il est aussi dans **les tests qui le forgent**. Une
modification de protocole se compte en TROIS endroits, pas deux.

---

## VÉRIFICATION DU PROTOCOLE v7 SUR TOUTES LES PORTES RÉPARTIES — FAITE (11 octobre 16 h 30)

Le v7 change la **mise en page de la trame**, donc **toutes** les exécutions à deux nœuds. Les
huit portes qui parlent le protocole ont été rejouées après le changement :

| porte | résultat |
|---|---|
| `porte-flux.sh` (les deux côtés, 5 modes) | **code 0** — écarts inchangés : 0,00e0 · 0,00e0 · 3,65e-2 · 0,00e0 · 4,45e-3 |
| `porte-pannes.sh` | **code 0** — pannes nommées, code 7 |
| `porte-registre.sh` | **code 0** |
| `porte-budget.sh` | **code 0** — budgets d'octets et de latence |
| `porte-pont.sh` | **code 0** — fibres, falaise, symétrie |
| `porte-coupe.sh` | **code 0** — points de coupe |
| `porte-bus-socket.sh` | **code 0** — bus par le réseau |
| `porte-horloge.sh` | **code 0** — bornes de pas |
| `porte-fusion.sh` | **code 0** — fusion des traces |

**Huit vertes, aucune rouge, 122 tests verts.** Un en-tête décalé d'un octet aurait fait tomber
la première ; les sept autres vérifient que le reste du contrat (pannes, budgets, fibres,
registre, bus, horloge, traces) n'a pas bougé.

**Ce qui attend son premier round** : le **compte de paires côté nœud** (même mécanisme que le
v7 : un champ dans la trame de réponse, protocole v8) pour clore le budget `paires/s` — le
troisième volet de C10, dont les octets et la latence sont déjà faits.

---

## PROTOCOLE v8 — LIVRÉ (11 octobre 18 h) : le compte de paires du nœud voyage

Trois modifications de plus que la spécification ne prévoyait pas, et l'une est un **bug de ma
part attrapé par la mesure** :

1. le compteur du nœud est **CUMULATIF** ; je l'additionnais à chaque trame, donc la somme des
   cumuls valait N²/2 — le pilote annonçait **4 293,9 M par pas** au lieu de 178,9 ;
2. c'est **la comparaison au chiffre connu** (358 M par jeton pour le modèle ENTIER, §21 de la
   campagne) qui l'a rendu visible : 12× plus que le modèle complet pour la moitié de ses
   couches ne pouvait pas être juste ;
3. corrigé (`fetch_max` au lieu de `fetch_add`), et le résultat est **178,9 M paires par pas**
   pour la moitié distante — la moitié des couches, la moitié des paires.

**Le pilote sait désormais ce que coûte la moitié distante**, annoncé par le nœud lui-même, sans
le déduire de son propre travail :

```text
paires du pair    : 8408924160 au total, 178.9 M par pas (annoncées par le nœud — protocole v8)
```

**Ce qui reste pour clore C10** : le `budget_paires` dans la topologie, comparé à ce compte par
pas, avec arrêt explicite (**code 9**) — le transport est fait, il ne manque que le contrôle.

**Vérifications** : `porte-flux.sh` **vert**, **122 tests verts**.

---

## PROTOCOLE v8 — SPÉCIFIÉ (11 octobre 17 h) : le compte de PAIRES du nœud

Objectif : clore le troisième volet de C10 (le budget `paires/s`). Les paires sont calculées par
**le nœud** ; le pilote ne peut donc pas les borner sans qu'elles lui soient **transportées**.

**Reconnaissance faite** : le compteur existe et est déjà exploité côté local.

```text
model.rs:2395   pub paires: [u64; 3],        // attention · experts · partagé
main.rs:1513    let pa = mdl.paires;         // le rapport le lit tel quel
main.rs:7299    let pt: u64 = pa.iter().sum::<u64>() + scores;
```

**Les six modifications, sur le patron du v7 (éprouvé au round 28) :**

1. **en-tête** : un `u64` (les paires dépassent 2³²) ⇒ `TAILLE_TETE` passe de **91 à 99** (huit
   octets, pas quatre) ;
2. `VERSION_FLUX` : **7 → 8** ;
3. `envoyer_flux` : écrire `paires` à l'offset **91** — mais **attention** : ce champ a un sens
   différent selon qui parle. Le pilote y met **0**, le nœud y met **son compte**. Le même
   en-tête sert aux deux sens, et un champ « qui ne veut dire quelque chose que dans un sens »
   doit être **écrit dans le commentaire** ;
4. `recevoir_flux` : lire `u64` à l'offset 91 ⇒ un champ `paires_du_pair` dans `Flux` ;
5. le pilote : accumuler et publier le compte du pair dans son rapport, à côté des octets ;
6. le budget : `budget_paires` dans la topologie du lien, comparé au compte **du pair** par pas —
   même conduite que les octets et la latence (arrêt explicite, **code 9**, aucune perplexité).

**Ce qui vérifie ce changement** : les mêmes huit portes réparties que pour le v7
(`porte-flux` en tête, qui fait parler les deux côtés sur cinq modes), plus un cas neuf pour le
budget de paires. Les tests de trame forgée **calculent** maintenant leur remplissage — c'est le
v7 qui l'a appris — donc seules les deux assertions « de mémoire » (taille, version) sont à
mettre à jour.

**Pourquoi ce n'est pas fait dans ce round** : le round 26 avait spécifié le v7, le 27 l'a tenté
et reverté, le 28 l'a livré. Le v8 suit exactement le même chemin, et ce round-ci est celui de la
spécification — avec, en plus, une difficulté que le v7 n'avait pas : **un champ directionnel**
dans un en-tête partagé.

---

## C10 — CLOS (11 octobre 20 h) : trois budgets, trois codes (6 · 8 · 9)

Le round précédent avait reverté ce travail après un déséquilibre d'accolades. **Repris en
ADDITIF** — rien supprimé, donc rien à casser — et livré :

| volet | code | mesure |
|---|---|---|
| octets | **6** | 1 860 octets pour un budget de 975 ⇒ arrêt au pas 0 |
| latence | **8** | 20,1 ms pour un budget de 1 ms |
| **paires** | **9** | **178 913 280** paires pour un budget de **1 000 000**/pas ⇒ arrêt **au pas 0** |

**La leçon du round précédent est appliquée** : le contrôle est **DANS la boucle**, au pas du
dépassement — et la porte l'exige (« aucune perplexité ne doit être rendue »). Placé après elle,
il laissait calculer et afficher la perplexité avant de refuser.

**Détail qui se recoupe** : le compte annoncé au PREMIER pas (178 913 280) vaut exactement la
valeur par pas mesurée sur la session entière (178,9 M) — un compteur cumulatif lu une fois dit
la même chose au début et à la fin.

**`porte-budget.sh` : 6 cas verts. `porte-flux.sh` : vert, 5 modes.**

---

## BUDGET DE PAIRES (C10, 3ᵉ volet) — TENTÉ (11 octobre 19 h), REVERTÉ : deux leçons

Le transport du compte de paires est livré (v8) ; il ne manquait que le **contrôle**. Tenté,
mesuré, puis **reverté** — l'arbre est propre et 122 tests passent.

**Ce qui a été écrit, et qui marche** : `budget_paires` dans la topologie du lien ; lecture par le
pilote ; comparaison du compte annoncé par le nœud au plafond `budget × pas` ; **refus en code
9**. Mesuré manuellement : budget généreux (10 G/pas) ⇒ le run aboutit et annonce **178,9 M
paires par pas** ; budget insuffisant (1 M/pas) ⇒ `PAIRES DÉPASSÉES … 8408924160 paires pour un
budget de 1000000 par pas sur 47 pas (plafond 47000000)`, **code 9** ✓.

**LEÇON 1 — LE CONTRÔLE DOIT ÊTRE DANS LA BOUCLE.** Placé après elle, il laissait **calculer et
afficher la perplexité** avant de refuser — soit exactement **le résultat partiel** que ce dépôt
refuse. C'est la **porte** qui l'a dit : son assertion « aucune perplexité ne doit être rendue »
a échoué. Le contrôle d'octets et celui de latence sont dans la boucle ; celui-ci doit y être
aussi.

**LEÇON 2 — UNE SUPPRESSION DE BLOC SE VÉRIFIE AUSSI.** Le déplacement du contrôle a laissé un
**déséquilibre d'accolades** qui a cassé la compilation ; plutôt que de bricoler un correctif sur
un fichier à moitié édité, **le round a été reverté**. Une modification de 7 sites qui ne compile
pas n'est pas une modification livrée — même règle que le v7 reverté au round 27, qui a été livré
au 28 après avoir été compris.

**Ce qui reste, précisément** : (1) `budget_paires` dans `topologie.rs` (champ + parse + le
littéral de test) ; (2) la lecture dans `run_ppl_reparti` ; (3) **le contrôle DANS la boucle**,
juste après la réception, avec `pas_servis` comme multiplicateur ; (4) le cas 6 de
`tools/porte-budget.sh`, déjà écrit, qui exige le code 9 **et l'absence de perplexité**.

---

## ÉTALONNAGE DE L'INSTRUMENT DE TRACE — FAIT (11 octobre 21 h) : 50 ms injectés, 50,2 ms mesurés

Toute la partie asynchrone (C4) repose sur une question préalable : **la trace globale sait-elle
mesurer le temps ?** Un instrument jamais étalonné ne prouve rien sur ce qu'il observe.

Protocole : un délai **connu** injecté (`"delai_ms": 50`), les deux côtés tracent, la fusion
apparie par `(lien, pas)`, et l'on compare l'horodatage d'**envoi** (pilote) à celui de
**réception** (nœud) :

| mesure | valeur |
|---|---|
| croisements par source | 46 (23 pas × 2 liens) |
| liens confrontés | **46 identiques, 0 divergents** |
| **écart envoi → réception, médian** | **50,2 ms** (min 50,2 · max 50,2) |
| délai injecté | 50 ms |

**L'instrument mesure le temps à 0,2 ms près** — et cet écart est le transport lui-même. Il est
**rigoureusement constant** (min = max) parce que le délai injecté l'est : un instrument bruité
l'aurait montré.

**Pourquoi c'est un préalable** : quand C4 dira que deux régions avancent à des rythmes
différents, l'instrument qui le dira aura été **étalonné contre une valeur connue**, et non
supposé juste parce qu'il produit des nombres.

---

## LA GIGUE D'UN PAS RÉPARTI — MESURÉE (11 octobre 22 h) : 7 ms sur 17,7 (40 %)

L'instrument étant étalonné (§ précédent), il peut mesurer autre chose que ce qu'on lui injecte.
La question qui décide de l'asynchronisme (C4) : **de combien la durée d'un pas varie-t-elle ?**
Un ordonnanceur qui suppose des pas réguliers casse à la première irrégularité.

| phase | médiane | p90 | max | min |
|---|---|---|---|---|
| aller (pilote → nœud) | **0,13 ms** | 0,14 | 0,16 | 0,09 |
| retour (nœud → pilote) | **0,14 ms** | 0,17 | 0,17 | 0,05 |
| **pas complet** | **17,67 ms** | 19,57 | **21,29** | **14,29** |

1. **le réseau local ne coûte rien** (0,13 / 0,14 ms) — cohérent avec la loi de latence de la
   campagne dès qu'un vrai RTT entre en jeu ;
2. **le pas complet vaut 17,67 ms**, dont l'essentiel est le calcul du nœud ;
3. **la gigue est de 7,00 ms sur 17,67, soit 40 %** — et le p90 dépasse la médiane de 2 ms.
   **Un ordonnanceur qui suppose des pas réguliers se trompe de 40 %** : c'est précisément ce que
   C4 devra absorber.

**Et avec un VRAI RTT** (`tools/proxy_latence.py`, 5 ms par message) — la condition laissée
ouverte est levée :

| phase | sans RTT | **avec 5 ms/message** |
|---|---|---|
| aller (pilote → nœud) | 0,13 ms | **5,29 ms** · p90 **10,38** (≈ 2× la médiane : le proxy endort par message, une trame qui traverse les deux sens paie deux fois → distribution **BIMODALE**) |
| pas complet | 17,67 ms | **30,24 ms** |
| **gigue** | 7,00 ms (40 %) | **14,80 ms (49 %)** |

**La gigue croît plus vite que la latence** : +71 % de latence médiane pour +111 % de gigue, et le
taux passe de 40 % à **49 %**. Donc **C4 doit tolérer la moitié d'un pas en irrégularité** sur un
lien à 5 ms — et la proportion **empire** avec la distance, l'inverse de l'intuition (« un lien
plus lent est plus régulier »).

**Ce que la mesure ne dit pas** : le proxy endort PAR MESSAGE ; il ne simule ni la perte, ni la
réorganisation, ni la congestion. La gigue mesurée est un **plancher** pour ce RTT.

---

## COMBIEN DE MESSAGES COÛTE UN PAS ? — MESURÉ (11 octobre 23 h 30) : quatre

Le protocole écrit la trame en **DEUX** fois (`write_all(&tete)` puis `write_all(&corps)`) : sur un
lien qui facture par message, ces deux écritures se paient deux fois. La pente délai → pas médian
donne le nombre équivalent de messages :

| délai par message | pas médian | pente |
|---|---|---|
| 0 ms | 14,87 ms | — |
| 2 ms | 23,35 ms | **4,24 messages** |
| 5 ms | 34,93 ms | **4,01** |
| 10 ms | 44,83 ms | **3,00** |

1. **à petit délai, un pas coûte ~4 messages** : en-tête ET corps, à l'aller ET au retour — le
   chiffre recoupe exactement les deux `write_all` de chaque direction ;
2. **la pente décroît avec le délai** (4,24 → 3,00) : ce n'est pas le protocole qui change, c'est
   le PROXY, qui endort après chaque `recv` et laisse le système regrouper. La mesure est donc un
   **majorant**, et le petit délai est le plus fidèle ;
3. **conséquence actionnable** : écrire en-tête et corps en **UNE** fois ferait payer ~2 messages
   au lieu de ~4 ⇒ sur un lien à 5 ms/message, **≈ 25 ms au lieu de ≈ 35 ms**, soit **−29 % de la
   durée du pas**, sans toucher ni au calcul ni aux octets.

**LA FUSION EST FAITE, ET ELLE PAIE** — les trois émetteurs écrivent **une seule trame**
(en-tête + corps concaténés) :

| délai/message | AVANT | **APRÈS** | gain |
|---|---|---|---|
| 2 ms | 23,35 ms | **19,06 ms** | **−18,4 %** |
| 5 ms | 34,93 ms | **27,98 ms** | **−19,9 %** |

La pente retombe à **2,62 messages** au lieu de 4,01 : le pas retrouve le nombre d'envois que le
protocole décrit vraiment. **−20 % de la durée d'un pas** sur un lien facturé par message, sans
toucher au calcul, aux octets ni au résultat — `porte-flux.sh` reste **vert** avec les cinq mêmes
écarts. **C'est le seul levier de ce sprint qui accélère sans rien coûter**, et il vient d'une
mesure.

**Et le gain est FIXE PAR ÉCHANGE** (~10 ms à 5 ms/message), donc il **pèse relativement moins**
quand l'échange transporte plus — mesuré en mode 3 (lots de 8 jetons, 28 772 octets par lot) :

| mode | temps par échange | gain |
|---|---|---|
| 0 (un jeton, 896 canaux) | 27,98 ms | **−20 %** |
| 3 (8 jetons, 28 772 octets) | 130,2 ms (dont 99,8 de calcul local) | **≈ −8 %** |

**La fusion paie donc d'autant plus que les pas sont petits** — et c'est le régime du décodage
jeton par jeton, celui où la latence domine.

**Ce qu'il ne dit pas** : le gain est nul sur un lien facturé **au débit** — la question « message
ou octet ? » est celle de l'opérateur. Mais le protocole ne doit pas **AJOUTER** de messages sans
raison.

---

## ▶ PROCHAINE ACTION (à lire en premier)

État au **11 octobre 6 h 45** · **21 portes, toutes vertes** (`tools/porte-*.sh`) ·
**122 tests verts** · 14 rounds livrés, tout poussé sur `origin/master`.

### La consigne tient : ne pas s'arrêter faute de liste

Le temps commun est la denrée la plus précieuse ; quand une liste s'épuise, la question est
« qu'est-ce qui est mesurable maintenant ? ». Un round qui **corrige** une mesure fausse vaut
un round qui en ajoute une — ce sprint en a produit cinq corrections, toutes documentées à
côté de la valeur d'origine.

### Les trois prochains chantiers, par valeur, avec leur première commande

**1. Le budget `paires/s` (C10, troisième volet).** Les octets et la latence sont faits ; il
reste les PAIRES, et elles se heurtent à une difficulté nommée : **ce sont les pairs qui les
calculent**, donc le pilote ne peut pas les borner sans que le nœud les lui TRANSPORTE. La
voie propre est d'ajouter le compte de paires du nœud à la trame de réponse (protocole v7) :
un champ, un contrôle, une porte. Commencer par mesurer ce que le nœud calcule réellement
par pas (il l'imprime déjà à la fin : « paires (poids × activation) : … par token »).

**2. C8 (suite) — une tête DÉDIÉE par profondeur.** Mesuré : un réflexe court ne peut pas
lire l'état intermédiaire (cos 0,145 à 16 couches sur 24). Il lui faudrait une tête
**entraînée pour sa couche** — c'est le même chantier que C7 vers les poids, et
`tools/entrainer_moteur.py` existe. Première commande : entraîner une tête linéaire sur
l'état de la couche 16 et mesurer son accord avec le modèle entier (le protocole de
`tools/porte-reflexe.sh` le fait déjà pour une tête empruntée).

**3. Les expériences de biologie E2/E4/E5** (`docs/biologie-pour-drave.md`) : croissance des
connexions, équilibre excitation/inhibition, rejeu. Le moteur a déjà les leviers
(`--ffn-gain`, `--act-thresh`, `--act-topk`, `--hebb-*`) et la campagne a mesuré les
réglages de parcimonie ; ce qui n'a pas été fait est la **courbe de dose** d'une inhibition
négative (`--ffn-gain` < 0) et son effet sur la perplexité, par couche.

### Ce qui a été livré (une ligne par capacité)

- **C1 / C4 / C5 / C5bis / C5ter / C10 / C11 / C12 / C12bis** : graphe de régions, borne de
  pas, bus (fichier **et** réseau), budgets **octets et latence**, pannes nommées
  (**codes 5/6/7/8**), **registre de régions**, trace globale, trace du nœud, fusion par le
  temps mural.
- **C2** : deux entrées se **somment** et la somme **arbitre** (7/7, jamais de 3ᵉ contenu) ;
  bascule à **α = 0,6** contre **0,509** prédit par les normes.
- **C6** : mémoire épisodique — trois négatifs, puis trois ingrédients (expansion,
  décorrélation, égalisation) : **élagage 83 %**, rappel 96,3 % à 50 % de dégradation,
  round-trip **exact**, Δ = **11 jetons sur 2 048**. Puis : le rappel **dépend de l'indice**
  (1 sur 8), il **n'est pas continu** (50 vs 1 006 pour deux jetons voisins), et la clé de
  **fenêtre** dégrade tout (prédiction réfutée) — **la sélectivité EST la netteté de la clé**.
- **C7** : consolidation — l'**exemplaire** bat la moyenne (7 % du magasin → 87 % de rappel),
  et le rejeu répété est un **point fixe exact** (0,00e0).
- **C9** : pont — **448 fibres = +2,81 % et ÷1,8 en octets**, falaise **entre 448 et 392** ;
  à budget égal **quantifier bat élaguer de 83 %** ; **où couper** : 8 coupes, une seule
  perplexité sans perte, et le coût du pont varie d'un **facteur 30**.
- **C2/C6 (la greffe)** : l'état injecté **transfère le contenu** quand il est prélevé **là où
  le calcul se fait** — et ma première conclusion négative était un **décalage d'un jeton**,
  corrigée et conservée à côté.

### Les cinq corrections de ce sprint, à ne pas réintroduire

1. **`--limit` diffère selon le chemin** : `--ppl` note les N **premiers** jetons,
   `--ppl-reparti` tronque aux N **derniers**. Dans une porte, `--limit` = **le nombre de
   jetons du fichier, compté** — les deux portes qui l'écrivaient à la main s'étaient
   trompées toutes les deux ;
2. **une position ne se devine pas** : `--tokenize` et `--prompt` ne comptent pas les mêmes
   jetons ⇒ `--etat-fin` (k-ième depuis la fin, résolu par le moteur, **après** troncature) ;
3. **`..Default::default()` donne 0,0** à un f32 : un poids de greffe par défaut à zéro
   n'aurait rien fait, en silence ;
4. **`sys.exit("message")` sort toujours en code 1** — une porte « verte » rendait 1 ;
5. **une porte qui échoue doit être instruite jusqu'à sa cause** : la rouge de répartition
   accusait le modèle, c'était la porte (255 jetons contre 128 annoncés).

---

## Objectif du sprint

Trois capacités du plan, chacune avec sa **porte mesurée** :

| # | capacité | porte (invariant à vérifier) | état |
|---|---|---|---|
| **C1** | **graphe de régions** : descripteur de topologie, validateur, ordonnanceur par dépendances, pilote multi-nœuds | un graphe **linéaire** rend des logits identiques **au bit près** ; un découpage à **trois régions** égale le modèle d'un seul tenant | ✅ **FAIT** — `topologie.rs` (8 tests) · la topologie pilote le découpage (0,00e0) · relais trois instances (0,00e0) · `tools/porte-topologie.sh` (5 cas, dont 2 refus) |
| **C9×C1** | **où couper** | le point de coupe change-t-il le résultat ou le coût ? | ✅ **FAIT** — **sans perte : 8 coupes, une seule perplexité (113,0068)** · **encodé : 8,9 % d'écart** · coût du pont de 448 fibres : **+0,52 % après 18 couches contre +17,09 % après 15** (facteur 30) ⇒ **couper tard** · portes `tools/carte_coupe.sh`, `tools/porte-coupe.sh` |
| **C12bis** | **fusion des traces** | deux processus qui se sont parlé doivent pouvoir être relus ENSEMBLE, dans un temps commun | ✅ **FAIT** — nœud tracé · v2 horodatée + mode · `--fusionner-trace` ordonne par le temps mural, mesure la dérive, confronte les deux bouts de chaque lien · porte `tools/porte-fusion.sh` (94 liens identiques ; 1 bit changé ⇒ **DIVERGENT**, code 3 ; v1 ⇒ refusée) |
| **C12** | **trace globale horodatée + rejeu** | rejeu d'une exécution distribuée == exécution, **0,00e0** | ✅ **FAIT** — `trace_globale.rs` (5 tests) · 126 croisements, **aucune divergence** · trace faussée d'un bit **détectée et nommée** · `tools/porte-trace.sh` |
| **C4** | **horloges par région** | un graphe sans cycle rend le **même résultat** qu'en synchrone ; les pas sont bornés et annoncés | 🟡 **premier pas FAIT** — compteur de pas par région · `--pas-max` borne la terminaison et **refuse de rendre un résultat partiel** (code 5) · porte `tools/porte-horloge.sh` · reste l'asynchronisme réel (avec C2) |
| **C5ter** | **bus par le réseau** | un réglage doit atteindre une AUTRE machine, pas seulement un autre fichier | ✅ **FAIT** — `--bus-serveur PORT` sur le pilote et le nœud, protocole `MODULATION canal valeur`, borné à 8 modulateurs, verrou pris une fois par ligne · porte `tools/porte-bus-socket.sh` (7 cas : socket ≡ statique **0,00e0**, neutre ≡ référence **0,00e0**, plein vol ≠ les deux) |
| **C5bis** | **diffusion du bus** | un canal poussé par un autre processus change l'exécution | ✅ **FAIT (fichier de contrôle)** — `--bus-fichier`, relu avant chaque trame · relais : 66,0379 contre 59,0790 · reste le transport par socket |
| **C3** | **délais par lien** | un délai change le **temps**, jamais un chiffre | ✅ **FAIT** — appliqué par le pilote ET par le nœud relais · porte `tools/porte-delais.sh` (même perplexité, empreintes identiques, +3,1 s pour 50 ms × 64 pas) |
| **C5** | **bus de modulation multi-canaux** | canal nul ⇒ sortie **inchangée** | ✅ **FAIT** — `bus.rs` (5 tests) · neutre ⇒ **empreintes identiques** · gain 1,5 ⇒ la sortie change · bus d'un **relais** ⇒ agit à travers les instances · `tools/porte-bus.sh` |

**Contraintes non négociables** : les **23 portes** du dépôt et les tests restent
verts ; le profil `release` reste le **binaire de mesure** (toute promotion se paie
d'un passage des portes) ; le crate reste **std seul, sans dépendance**.

---

## C1a — descripteur de topologie (FAIT, 9 octobre 17 h 10)

**Livré** : `drave-core/src/topologie.rs` (module autonome, ~420 lignes dont 8 tests) :

- **format JSON minimal**, analysé **à la main** (le crate est std seul) : objets,
  tableaux, chaînes, entiers — et *rien d'autre* ;
- **validation stricte** : trou de couverture, recouvrement de couches, identifiant
  dupliqué, lien vers une région inconnue, lien réflexif, **cycle** (refusé tant que
  la récurrence C2 n'existe pas), clé inconnue, mode de lien inconnu — chacun avec un
  message et un **code de sortie** ;
- **ordre d'exécution** par tri topologique de Kahn, et détection « chaîne *vs*
  graphe » (le cas de non-régression) ;
- **`Topologie::chaine()`** : la topologie déduite de `--couches-locales`, c'est-à-dire
  le pont entre l'existant et le graphe.

**Commandes et résultats vérifiés** :

```bash
drave --topologie /tmp/topo_chaine.json   # CHAÎNE · 2 régions · plan en 2 étapes
drave --topologie /tmp/topo_y.json        # GRAPHE · 3 régions · délai déclaré affiché
drave --topologie /tmp/topo_trou.json     # refus : « couche 12 n'est portée par aucune région » (code 3)
```

**La topologie se lit sans modèle** : la commande passe avant le chemin du GGUF, parce
qu'un descripteur de régions ne décrit pas des poids.

**Tests** : 8 (chaîne lue et validée, trou, recouvrement, cycle, clé inconnue, mode
inconnu, graphe en Y, chaîne du moteur). Suite complète : **85 tests**.

---

## C1b pas 1 — FAIT (9 octobre 17 h 20) : la topologie PILOTE le découpage

**Livré** : `--ppl-reparti … --topologie F` exécute désormais le découpage **décrit
par le fichier**, au lieu de le déduire de `--couches-locales`. Le pilote :

- lit et **valide** la topologie (les mêmes refus que C1a) ;
- exige **une** région locale et **une** distante (les chaînes de plus de deux
  régions demandent le relais, pas encore écrit — et il le dit) ;
- vérifie que la région locale **commence à la couche 0** (le pilote lit les jetons,
  il porte donc la première région) ;
- vérifie que les deux régions **recouvrent le modèle entier, sans trou** — le nombre
  de couches est lu dans l'**en-tête** du GGUF, sans charger les poids ;
- **refuse** une topologie dont l'adresse contredit `--ppl-reparti` : deux sources
  pour la même chose qui se contredisent ne doivent pas se mesurer en silence.

**La porte, outillée** : `tools/porte-topologie.sh`, quatre cas —

| cas | résultat mesuré (m5_d384_dense, 2 couches locales sur 4) |
|---|---|
| 1. référence, modèle entier | perplexité **3,7326** |
| 2. découpage historique (`--couches-locales`) | **5,0374** · écart de flux **0.00e0** |
| 3. **découpage par TOPOLOGIE** | **5,0374** · écart **0.00e0** — *même chiffre* |
| 4. refus | trou de couverture → refusé · adresse contredite → refusée |

**Verdict : PORTE TENUE.** La topologie rend le même chiffre que le découpage
historique, au chiffre près, et l'écart de flux reste **0,00e0**.

*(Note : `--topologie` seul imprime le plan et sort ; `--ppl-reparti … --topologie`
exécute. La pré-analyse a dû être restreinte pour que les deux usages coexistent —
sans quoi la commande imprimait le plan au lieu de mesurer.)*

### Ce qui reste pour C1b : le RELAIS (trois instances)

Conception ci-dessous, inchangée. C'est le jalon qui donne « trois régions sur trois
instances », et donc la **distribution sur plusieurs instances** demandée.

---

## C1b pas 2 — **FAIT (9 octobre 18 h)** : le RELAIS, trois régions sur trois instances

**Livré** : un nœud du milieu (`--flux-serveur … --topologie F --region n1`) applique
**sa** plage (celle que la trame lui donne), puis **transmet à son successeur** au
lieu de répondre à son appelant ; le retour se fait de proche en proche. Le pilote,
lui, accepte désormais une **chaîne de régions distantes** : la première est le pair
direct, les suivantes sont atteintes par relais.

**La porte, mesurée** (`tools/porte-topologie.sh`, cas 5 — modèle à 24 couches,
mode 0 f32) :

| montage | perplexité | écart de flux |
|---|---:|---:|
| référence locale (mêmes réglages) | 42,5477 | — |
| **deux régions / deux instances** | **42,5477** | **0.00e0** |
| **trois régions / trois instances** (pilote + relais + sortie) | **42,5477** | **0.00e0** |

**PORTE TENUE : le relais ne change pas un chiffre.** Deux nœuds distants servent
127 trames chacun, et le résultat est identique au découpage à deux régions comme à
la référence locale.

### Le bug que cette étape a trouvé — et la porte qui l'a attrapé

En câblant la plage du pair, j'ai envoyé `derniere` au lieu de `derniere + 1` : **la
fin de plage est EXCLUSIVE** (le nœud fait `couche_fin = f.fin` et exécute
`debut..fin`). Conséquence : la dernière couche de la région distante n'était plus
exécutée — et **le défaut ne touchait que les modes 0, 1 et 2** (les modes 3 et 4
passent par un autre encodeur, intact).

C'est `tools/porte-flux.sh` qui l'a dit, en trois lignes :

```
mode 0 — f32 dense            1.69e1  ❌ (plafond 0)     -> après correctif : 0.00e0 ✅
mode 1 — listes quantifiées   1.69e1  ❌                -> 0.00e0 ✅
mode 2 — listes par blocs     1.67e1  ❌                -> 3.65e-2 ✅
```

**Leçon de méthode, à appliquer pour tout le sprint** : toute modification du chemin
d'exécution se paie d'un **passage de `porte-flux.sh`** — cinq modes, deux minutes —
et sans lui, trois modes sur cinq seraient restés cassés en silence.

---

## C1b pas 3 (conception d'origine, pour mémoire) — le relais : points d'insertion

**Ce que le protocole permet déjà, et c'est beaucoup.** Une trame porte la **plage de
couches à appliquer** (`f.debut`, `f.fin`), le mode, la position, et la charge ; le
nœud applique `mdl.forward(0, f.pos)` **sur sa plage** puis renvoie l'état sur le
même socket (`envoyer_flux`, main.rs:3351). Autrement dit, **le découpage est déjà
transmis par le flux** : rien à inventer côté format.

**Ce qui manque : le RELAIS.** Aujourd'hui un nœud rend toujours la main à son
appelant. Une chaîne à trois régions sur trois instances demande qu'un nœud du milieu
**transmette à son successeur** au lieu de répondre.

**Les points d'insertion, relevés :**

| où | quoi |
|---|---|
| `run_serveur_flux`, après `let sortie = mdl.forward(0, f.pos as usize);` (**main.rs:3347**) | si `--relais` est déclaré : ouvrir une connexion vers le successeur, lui envoyer la trame de **sa** plage, lire sa réponse (`recevoir_flux`, main.rs:2977), et renvoyer **cette** réponse à l'appelant — au lieu de `sortie` |
| `run_ppl_reparti` (**main.rs:3605**) | la plage et l'adresse du pair viennent de la **topologie** (première région distante) au lieu de `--couches-locales` et du pair unique |
| `Options` (main.rs:562) | `relais: Option<String>`, `region: Option<String>` (côté nœud) et `topologie: Option<String>` (côté pilote) |
| `topologie.rs` | `Topologie::successeur(id)` et `Topologie::region(id)` — deux accesseurs, déjà presque écrits (`est_une_chaine`, `valider`) |

**Le format de trame n'a pas à changer** : le relais réexpédie une trame de même
mode, avec la plage de son successeur. Le retour se fait de proche en proche, chaque
nœud rendant sur son socket entrant — donc **le pilote n'a rien à savoir du nombre de
relais**.

**Protocole de mesure de la porte** (à écrire dans `tools/porte-graphe.sh`, sur le
modèle de `tools/porte-reparti-moteur.sh`) :

1. référence : le modèle **entier**, un seul processus, même mode et même `--abits` ;
2. **deux régions / deux instances** : doit reproduire l'écart **0,00e0** d'aujourd'hui
   (non-régression du chemin existant) ;
3. **trois régions / trois instances** (pilote + deux nœuds en relais, ports
   distincts sur localhost) : la perplexité doit être **la même** que la référence ;
4. et la même chose derrière le **relais de latence** (`tools/proxy_latence.py`), pour
   vérifier que les délais ne changent pas le résultat — seulement le temps.

**Ce qui reste hors de C1b, et il faut le dire** : les régions **non contiguës** et
les **entrées multiples** (un graphe en Y qui s'exécute) demandent que le moteur
sache tenir deux plages disjointes dans un même processus — c'est la capacité **C2**
du plan, pas C1.

---

## C12 — FAIT (9 octobre 18 h 40) : trace globale et rejeu exact

**Livré** : `drave-core/src/trace_globale.rs` (5 tests) + deux drapeaux —
`--trace-globale F` (le pilote écrit ce qui traverse chaque lien) et
`--verifier-globale F` (il rejoue et compare).

**Ce qui est enregistré** par croisement : région, pas, lien, nombre de valeurs,
**empreinte FNV-1a des octets** (donc au **bit près**, sans epsilon) et horodatage.
Les valeurs elles-mêmes ne sont **pas** stockées : 126 croisements tiennent en 128
lignes de texte, et la trace dit *où* regarder — le rejeu recompte et compare.

**La porte** (`tools/porte-trace.sh`), trois cas mesurés :

| cas | résultat |
|---|---|
| 1. exécution répartie + trace | **126 croisements** écrits (64 pas × 2 liens) · perplexité 59,0790 |
| 2. rejeu de la même exécution | **126 croisements, AUCUNE divergence ✅** |
| 3. trace **faussée d'un seul bit** | **DÉTECTÉE** : « DIVERGENCE AU BIT PRÈS au croisement 0 — région « local », pas 0, lien « local->pair » : empreinte 0x…d696 attendue, 0x…d697 obtenue » |

**Le cas 3 est le plus important** : une porte qui ne sait pas échouer ne vérifie
rien. La vérification nomme le pas, la région et le lien — c'est exactement ce qui
manquait pour déboguer un graphe distribué.

---

## C9 × C1 — FAIT (10 octobre 9 h) : OÙ COUPER le modèle ?

`tools/carte_coupe.sh` + `tools/porte-coupe.sh` (3 cas). La question n'avait jamais
été posée : C1 et C9 étaient mesurés à **un seul** point de coupe (12/12).

1. **Avec un lien SANS PERTE, le point de coupe ne change RIEN** : les huit coupes
   (4, 6, 8, 10, 12, 15, 18, 20 couches locales sur 24) donnent **113,0068** — huit
   fois la même valeur. L'invariant de C1 est donc vérifié sur huit coupes.
2. **Avec un lien ENCODÉ, les mêmes coupes s'écartent de 8,9 %** (108,87 à 118,53) :
   c'est l'**erreur de quantification** du lien qui dépend de la profondeur. Trois
   coupes sur quatre font même *mieux* que le lien sans perte (108,87 contre 113,01).
3. **Le coût d'un pont de 448 fibres dépend du point de coupe, d'un facteur 30** :
   **+0,52 %** en coupant après 18 couches, +2,81 % après 12, **+17,09 %** après 15.
   Le milieu n'est pas le bon endroit, et l'état de la couche 18 est manifestement
   **redondant** là où celui de la couche 15 ne l'est pas — cohérent avec C8 (la
   direction se construit tardivement : cos 0,145 à 16 couches, 0,320 à 20).

**Conséquence pour distribuer** : couper **tard** quand le lien est étroit, et mesurer
le coût du pont **au point de coupe choisi** (il varie d'un facteur 30 sur le même
modèle).

**La porte** : 3 cas — lien sans perte ⇒ une seule perplexité sur 8 coupes · lien
encodé ⇒ écart ≥ 2 % (témoin, sinon le cas 1 serait vrai « parce que rien ne change
jamais ») · le coût du pont varie d'un facteur ≥ 3 selon la coupe.

**Erreur attrapée par la porte** : elle passait `--pont-k` au pilote mais **pas au
nœud**, donc mesurait un pont asymétrique (+4,92 % là où le pont symétrique coûte
+2,81 %). Comparé à `porte-pont.sh`, qui le passait bien.

---

## C8 (premier pas) — FAIT (10 octobre 8 h 20) : le réflexe, et il ne sait rien

**La question** : un réflexe est un chemin COURT (la moelle épinière ne remonte pas au
cortex). Le moteur sait déjà tronquer (`--couches 0,L` + `--tete-partielle`) ; la
question mesurable est donc **à partir de quelle profondeur un réflexe tombe-t-il
d'accord avec le modèle entier ?** Mode `--reflexe-essai N`, porte
`tools/porte-reflexe.sh`.

| couches | accord | **cos(état tronqué, état final)** | plus rapide |
|---|---|---|---|
| 1 | 0,0 % | 0,044 | 18,5× |
| 8 | 0,0 % | 0,058 | 2,6× |
| 16 | 0,0 % | 0,145 | 1,3× |
| 20 | 6,2 % | 0,320 | 1,0× |
| **24** | **100,0 %** | **1,000** | — |

**Il n'y a pas de sortie précoce utilisable** : 0 % d'accord jusqu'à 16 couches sur 24,
et il ne décolle qu'à 24 — quand le réflexe *est* le modèle. Le gain de temps est réel
(18,5×), donc ce n'est pas un artefact. **Et la cause est mesurée** : l'état
intermédiaire est **presque orthogonal** à l'état final (cos 0,145 à 16 couches). La
tête du modèle est celle de sa dernière couche et lit une direction que seules les
dernières couches produisent — un réflexe court ne peut pas réutiliser cette tête, il
lui faudrait **sa propre** lecture entraînée, ce que le moteur ne sait pas produire.
C'est un **manque**, et il est écrit comme tel.

**Conséquence pour la distribution** : on ne peut pas accélérer un graphe en sortant
plus tôt d'une région ; le chemin est au moins aussi long que le modèle.

**La porte** : 4 cas — le réflexe à profondeur entière EST le modèle (100 %) · aucune
sortie précoce sous 2/3 de la profondeur · la cause est la direction (cos < 0,5) · le
gain de temps est réel (≥ 3×, sans quoi la mesure n'aurait pas de sens).

---

## C2 — FAIT (10 octobre 16 h) : DEUX ENTRÉES, UNE RÈGLE DE MÉLANGE — et la correction d'un faux négatif

**La question de C2, sans toucher au moteur** : deux flux qui se rencontrent, que devient
leur contenu ? Une somme de deux états s'écrit avec `--fusion-etat` ; la mesure dit ce que
le calcul en fait.

**D'abord la correction, et elle est importante.** La porte `porte-greffe` concluait
« une greffe d'état ne transfère pas le contexte » : l'état de A injecté dans B ne rendait
jamais le code. **C'était un artefact d'un décalage d'un jeton** — le prélèvement se
faisait sur les identifiants tokenisés (1 750) alors que l'inférence construit une invite
d'**un jeton de plus** (1 751), donc on injectait l'état qui prédit « : » au lieu du code.
Avec `--etat-fin` (k-ième depuis la fin, résolu dans la numérotation de l'inférence) :

| état injecté dans une invite SANS aucun code | réponse |
|---|---|
| état final de A (code `ZQ-4471-KX`) | **`ZQ3`** |
| état final de B (code `KJ-9999-QP`) | **`K00`** |

**Le contenu passe.** Trois mesures ont échoué sur ce décalage avant que `--etat-fin`
n'existe ; la leçon est écrite : **une position ne se devine pas, elle se capture là où
le calcul se fait**.

**La règle de mélange, mesurée** (deux invites de 1 750 jetons, même remplissage, même
question, un code différent) :

| α (poids de A) | norme du mélange | réponse |
|---|---|---|
| 0 | 65,89 | `K00` (B) |
| 0,2 | 64,10 | `K00` |
| 0,4 | 62,95 | `K00` |
| 0,5 | 62,63 | `K00` |
| **0,6** | 62,49 | **`ZQ3` (A)** |
| 0,8 | 62,72 | `ZQ3` |
| 1 | 63,65 | `ZQ3` |

1. **la somme ARBITRE, elle ne détruit pas** : sur les sept mélanges, la réponse commence
   toujours par le premier jeton de l'un des deux contenus — jamais un troisième ;
2. **le point de bascule est à α = 0,6**, et la prédiction par les **normes**
   (|B|/(|A|+|B|) = 65,89/129,54 = **0,509**) tombe à 0,091 : la somme est donc arbitrée
   par la **norme** des états, pas seulement par le poids qu'on leur donne ;
3. conséquence pour C2 : une fusion par somme est utilisable, mais **son seuil se règle
   en normes** — deux entrées de tailles différentes ne pèsent pas pareil à poids égal.

**Portes** : `tools/porte-melange.sh` (nouvelle, 4 cas) et `tools/porte-greffe.sh`
(corrigée : le cas 4 attend maintenant le contenu, et l'ancienne conclusion est conservée
à côté de la correction).

---

## C2/C6 — (premier texte, conservé) la greffe d'état, et ce qu'elle ne transférait PAS

**Le passage manquant** : C6 retrouve un état par son contenu, C9 limite ce qui traverse
un lien — mais si l'on **injecte** l'état d'un moment vécu dans un calcul qui ne l'a pas
vécu, l'information est-elle encore là ? Ajouté par `--fusion-etat`, `--fusion-pos`
(dont la valeur symbolique **`dernier`**), `--fusion-alpha`, et `--etat-sortie` /
`--etat-pos` (prélèvement, **plusieurs positions en une passe**).

Protocole décisif — deux invites qui ne diffèrent que d'une phrase : A contient
« IMPORTANT : the vault access code is ZQ-4471-KX. », **B est le même texte sans
l'aiguille**. Le 0,5 B répond `ZQ-4471-K` à A et `150px` à B.

| cas | mesure |
|---|---|
| témoin, poids **0** | **identique** à B sans greffe |
| A + son propre état, poids 100 | `25, 57, 48, 12, 19, …` — le contenu de A est là |
| **B + l'état de A**, poids 1…100 | **jamais le code** |
| B + l'état de A **partout**, poids 100 | `25,25,25,…` — dégénéré |

**Une greffe d'état n'est pas une greffe de contexte.** Et la cause est mesurée : le
**premier** jeton change (`220 → 25`, il vient de l'état injecté) mais **la suite reste
celle de B** — les jetons suivants sont **re-dérivés par l'attention sur le cache KV**,
que la greffe ne touche pas.

**Conséquence** : pour qu'une mémoire **serve**, elle doit entrer comme **contenu** (RAG)
ou comme **entrée de cache** — et le moteur n'a **aucune prise sur le cache KV**. Manque
écrit comme tel.

**Trois pièges attrapés en chemin**, tous de la même famille — un drapeau qui n'agit pas :
1. `..Default::default()` donnait **0,0** à `--fusion-alpha` : une greffe aurait injecté
   un vecteur multiplié par ZÉRO, en silence (corrigé en 1,0) ;
2. la position de la dernière invite **ne se devine pas** : `--tokenize` et `--prompt` ne
   comptent pas les mêmes jetons (l'espace initial), la greffe mordait un jeton du MILIEU
   (d'où la valeur symbolique `dernier`, résolue par le moteur APRÈS la troncature) ;
3. `DRAVE_DEBUG_FUSION` lue mais non déclarée : le test `VARS_LUES` du dépôt l'a
   attrapée immédiatement.

**La porte** : `tools/porte-greffe.sh`, 5 cas (témoin de non-effet · mécanisme vérifié
sur A · le négatif à cinq poids et à toutes les positions · la cause par la suite qui
reste celle de B).

---

## C9/C10 (premier pas) — FAIT (10 octobre 7 h) : le pont à fibres limitées

**La question du corps calleux, posée en termes mesurables** : deux régions échangent
un état à chaque pas ; **combien faut-il en échanger pour ne rien perdre ?**
`--pont-k K` ne garde que les K plus grandes amplitudes, **dans les deux sens** (le
nœud reçoit le même réglage), et le moteur publie les octets réellement échangés.

**Deux pièges, tous les deux trouvés par la porte :**

1. le pont n'était appliqué **que du pilote vers le nœud** — la mesure le disait sans
   ambiguïté (1 096 octets à l'aller contre 1 959 au retour). Un corps calleux à
   moitié coupé n'est pas un pont ;
2. **en dense f32, élaguer ne réduit AUCUN octet** : 3 664 octets avant comme après,
   avec **+7,83 %** de perplexité à 448 fibres. C'est l'**encodage** qui convertit la
   parcimonie en octets.

**La courbe utile (listes par blocs)** :

| fibres | perplexité | octets/flux | écart |
|---|---|---|---|
| 896 | 111,9225 | 1 951 | — |
| 672 | 112,9891 | 1 543 | +0,95 % |
| **448** | **115,0632** | **1 096** | **+2,81 % (÷1,8 en octets)** |
| 224 | 233,8589 | 648 | **+108,9 %** |
| 112 | 1 153,3098 | 424 | +930,5 % |

**On peut couper le pont en deux (+2,81 %, ÷1,8 en octets), pas en quatre** : la
falaise est **entre 448 et 224 fibres**. Et **à budget égal, quantifier bat élaguer** :
le rendement (perplexité pour 1 000 octets) est de 57,4 pour l'encodage complet contre
105,0 pour le pont de 448 fibres — **83 % pire**. Même conclusion que pour les poids :
garder les canaux et réduire leur précision vaut mieux que jeter des canaux.

**La porte** : `tools/porte-pont.sh`, 7 cas (pont entier ≡ sans pont dans les **deux**
encodages · les deux sens maigrissent · **monotonie** sur 5 points · élaguer coûte ·
le piège du dense f32 vérifié comme tel · rendement comparé à budget égal).

**Ce qui reste** : localiser la falaise entre 448 et 224 fibres (336 ? 280 ?), et
refaire la courbe sur un modèle plus large — le même *nombre* de fibres y représente
une fraction plus petite de l'état.

---

## C6 — FAIT (10 octobre 01 h 50) : mémoire épisodique, et ce qu'elle ne sait pas faire

**Le module** (`drave-core/src/episodique.rs`, 8 tests) : clé **creuse** (k-WTA sur
l'amplitude), **index inversé** canal → épisodes, écriture **en une passe**, lecture
par recouvrement maximal, magasin écrit en **bits** (donc round-trip exact par
fichier). Le mode `--episodique-essai N` collecte de **vrais états** du modèle et
mesure quatre choses : round-trip, séparation, nouveauté, rappel.

**Ce qui marche (sur 300 états réels, k = 64/896) :**

- **round-trip 300/300 AU BIT PRÈS**, y compris après passage par le disque
  (300/300 lectures identiques) ;
- **rappel** 100 % (indice intact) → 96,7 % (25 % dégradé) → 69,3 % (50 %) →
  15,3 % (75 %), hasard 0,33 % ;
- **nouveauté** : 41,5/64 pour un indice jamais écrit contre 64/64 pour un connu —
  le magasin distingue « je me souviens » de « ça ressemble », mais **le pire des
  nouveaux atteint 57/64** : des faux positifs existent.

**Les trois résultats négatifs, qui sont les plus utiles :**

1. **l'index inversé n'élude RIEN** : chaque lecture examine 300 candidats sur 300.
   Deux états différents partagent **23,9 canaux sur 64** (37 %), très au-dessus du
   hasard (k²/dim = 4,6) : toute clé recouvre tout le magasin. Le coût réel d'une
   lecture est donc un balayage complet (N × k comparaisons), et c'est la **mémoire**
   du magasin (N × dim × 4 octets) qui limite, pas le temps ;
2. **l'espacement des états ne change rien** (24,03 contre 23,88 pour un état tous
   les 8 jetons) : la corrélation n'est **pas** un effet de voisinage de texte.
   L'hypothèse naturelle est fausse, et elle est réfutée par la mesure ;
3. **à petit k, l'invariant du plan CASSE** : k = 8 → **81 des 300 états partagent
   la clé d'un autre** et le round-trip tombe à **219/300**, *tous* les échecs
   expliqués par ces collisions (k = 16 : 288/300 · k = 32 : 299/300 · k = 64 :
   300/300). L'invariant « écrire puis relire rend la valeur écrite » **n'est pas une
   propriété du code, c'est une propriété du couple (données, k)** — la porte le
   vérifie au lieu de le supposer.

**La décorrélation** (moyenne des états retirée) **aide la qualité** — séparation
23,9 → 20,3, nouveauté 41,5 → 37,5, rappel à 50 % 69,3 → **78,3 %** — **sans
élaguer davantage** (100 %). L'arithmétique dit pourquoi : 300 × 64 = 19 200 entrées
sur 896 canaux, soit ~21 par canal ; une clé de 64 canaux touche ~1 340 entrées et
couvre donc tous les épisodes.

**La porte** : `tools/porte-episodique.sh`, 5 cas (round-trip exact · disque ·
monotonie du rappel · nouveauté · **collisions qui expliquent tous les échecs à
k=8**), et elle finit en annonçant ses conditions.

**L'expansion, faite, et elle a demandé TROIS ingrédients** (suite du même round) :

| configuration (300 états) | séparation | candidats | rappel 50 % | rappel 75 % |
|---|---|---|---|---|
| 896 canaux, k = 64 | 23,9/64 | 300/300 (0 % éludé) | 69,3 % | 15,3 % |
| 16 384 canaux, k = 64 | 9,0/64 | 267/300 (11 %) | 48,7 % | 10,3 % |
| **16 384 + canaux ÉGALISÉS** | **0,38/64** | **51/300 (83 % éludé)** | **96,3 %** | **69,0 %** |
| **idem, N = 2 500** | 0,30/64 | 468/2 500 (**81 %** éludé) | 95,6 % | 66,0 % |
| **idem, 3 corpus, N = 240** | 1,22/64 | 35/240 (**85 %** éludé) | 95,0 % | 73,8 % |

L'expansion **seule** améliore la séparation mais n'élude presque pas : quelques
canaux sont systématiquement grands (la projection les rend sensibles à une direction
commune), ils entrent dans presque toutes les clés et leurs listes deviennent des
**hubs** (7× la moyenne) — toute clé d'indice tombe sur eux. **Centrer et réduire
chaque canal de clé sur le magasin** (une égalisation d'usage — ce que le gyrus denté
obtient par normalisation et inhibition latérale) fait tomber la séparation à
**0,38/64**, le plancher du hasard pour 64 canaux sur 16 384 étant 0,25.

**Le coût de l'expansion est FIXE, celui du balayage croît** : 131 072 additions par
lecture contre N × 64 comparaisons ⇒ rentable au-delà de **N ≈ 2 048 épisodes**, et
**en dessous, le balayage complet est moins cher**. Le programme l'écrit lui-même.

**C7 suite — le rejeu RÉPÉTÉ est un POINT FIXE, pas une usure :** mesure sur 8 et 12
cycles (seuils 4 et 8) — du cycle 2 au cycle 12, **rien ne bouge** : mêmes 107 (ou 154)
prototypes, même compression (35,7 % / 51,3 %), même rappel d'appartenance (93,0 % /
95,3 %) mesuré **contre les épisodes d'origine** (appartenances composées à travers les
cycles), et une erreur **exactement nulle (0,00e0)**. Après une consolidation, chaque
prototype est son propre exemplaire : plus rien à fusionner. **Rejouer une mémoire ne
l'use pas** — contrairement au rejeu vers les poids avec une mauvaise règle (8,8246
contre 8,3869). Cas 8 dans `porte-episodique.sh`.

**C6 suite — un indice ÉTRANGER : effet réel, NON ROBUSTE (corrigé par la porte)** :
`--episodique-indice` accepte un état **extérieur** au magasin. La distinction est
essentielle : un indice pris DANS le magasin s'y retrouve lui-même (recouvrement 64/64)
et ne teste rien — la première version de cette mesure tombait dans ce piège.

| indice | rendu | recouvrement | distance à l'aiguille (740) |
|---|---|---|---|
| la question, prise dans le magasin | 1749 (elle-même) | 64/64 | 1 009 jetons (hasard 448) |
| la question, **EXTÉRIEURE** (contexte sans l'aiguille) | 604 | **4/64** | **136 jetons** |

**Et la porte a corrigé la conclusion** : en écrivant `tools/porte-indice.sh`, la
question a été écrite avec un **point d'interrogation** de plus — et le même protocole
donne alors **378 jetons** au lieu de 136 (hasard 448). L'effet existe, il n'est **pas
robuste** : il dépend de la formulation exacte de l'indice. La porte n'exige donc que
« mieux que le hasard » et **affiche un avertissement** quand la marge est faible, au
lieu de figer un chiffre qui ne tient pas. Ce qui reste solide : l'écho (64/64), la
complétion de motif, et la localisation quand l'indice vient du contenu cherché.

**C6 suite — la mémoire LOCALISE, et la mesure est en jetons** : ajout de l'erreur
**moyenne en jetons** entre l'épisode rendu et l'épisode interrogé (les épisodes sont
numérotés dans l'ordre du texte, donc la distance entre identifiants *est* une
distance en jetons).

| N | rappel 25 % | rappel 50 % | rappel 75 % | Δ à 50 % | Δ à 75 % | élagage |
|---|---|---|---|---|---|---|
| 300 | 100 % | 96,3 % | 69,0 % | **2 jetons** | 24 | 83 % |
| **2 048** | 99,9 % | 95,4 % | 64,5 % | **11 jetons** | 86 | 81 % |

**La précision relative s'améliore avec la taille** (0,67 % du texte à 300, 0,54 % à
2 048) : quand la mémoire se trompe, **elle se trompe de près**. C'est la propriété qui
rend la mémoire utilisable pour *situer* un passage — elle n'a pas besoin d'être exacte
pour servir. Sur 2 048 épisodes : round-trip **2 048/2 048 au bit près**, séparation
0,37/64, indice jamais écrit 8,8/64 contre 64/64, et la consolidation en mode
**exemplaire** donne 62,5 % du magasin pour 93,4 % de rappel.

**C7 (premier pas) — CONSOLIDER PAR REJEU, et un résultat net :** rejouer les
épisodes et **fusionner ceux dont les clés co-activent**. Deux façons de faire le
prototype, et elles ne se valent pas (300 états, seuil 1) :

| prototype | prototypes | compression | rappel d'appartenance |
|---|---|---|---|
| **MOYENNE** (un point abstrait) | 39 | 13,0 % | **22,3 %** |
| **EXEMPLAIRE** (un cas réel) | 21 | **7,0 %** | **87,0 %** |

À seuil 8 : moyenne 66,7 % du magasin → 34,0 % de rappel ; exemplaire 51,3 % →
**95,3 %**. **Le mécanisme** : la clé d'une moyenne est recalculée depuis un point
qui n'a jamais existé, donc elle ne coïncide avec la clé d'aucun membre ; un indice
venu d'un membre ne retrouve plus son prototype (et à seuil 2 la moyenne rappelle
*moins* qu'à seuil 1 : elle s'éloigne en agrégeant). **Abstraire par moyennage
détruit la rappelabilité** — c'est une propriété de la clé, pas une opinion. Ce que
C7 au sens du plan (rejouer pour modifier des POIDS) n'est **pas** : le moteur
n'entraîne pas, et les règles locales existantes ont été mesurées dégradantes.

**Et le résultat tient sur plusieurs documents** (240 états de 3 corpus : code,
français, multilingue, cache neuf à chaque) : round-trip **240/240**, élagage 85 %,
rappel 99,2 / 95,0 / 73,8 %. La mémoire stocke les **états exacts** ; seule la clé
est dilatée. **Reste non mesuré** : la reconstruction d'un état depuis une clé
dilatée, le rappel après consolidation, et le recalcul des statistiques d'égalisation
quand le magasin grandit.

---

## C5ter — FAIT (10 octobre 00 h 20) : le bus par le réseau

**Pourquoi C5bis ne suffisait pas.** C5bis diffusait un réglage par un **fichier**
relu à chaque pas — donc il fallait un système de fichiers partagé, c'est-à-dire
**pas deux machines**. Un bus qui n'atteint pas la deuxième machine n'est pas un bus
distribué, c'est un fichier de configuration.

**Ce qui est fait :** `--bus-serveur PORT` sur le pilote **et** sur le nœud. Le
protocole est celui du fichier — `MODULATION canal valeur`, une ligne par réglage —
donc rien de nouveau à apprendre, et les mêmes validations (valeur absente, non
finie, ligne malformée : refusées **avant** d'entrer dans le calcul). Le bus est relu
**à chaque pas** côté pilote comme côté nœud : une modulation à mi-parcours change la
suite du calcul, pas le passé.

**Ce qui est borné, et pourquoi :** un fil par connexion (un modulateur muet ne doit
pas bloquer les autres), borné à **8** modulateurs (des connexions sans fin ne
doivent pas créer des fils sans fin) ; au-delà, la connexion est refusée en le
disant. Le verrou du bus est pris **une fois par ligne reçue**, jamais gardé pendant
le calcul — le garder aurait bloqué le fil d'écoute pour toujours.

**La porte** (`tools/porte-bus-socket.sh`), 7 cas, chaîne à **trois** régions :

| cas | mesure |
|---|---|
| 1. référence, aucun bus | 113,0068 |
| 2. bus **statique** sur le nœud du milieu | **148,7080** — le bus est branché |
| 3. bus par **socket**, ligne avant le pas 0 | **148,7080** · écart au statique **0,000000e+00** |
| 4. ligne **neutre** par socket | écart à la référence **0,000000e+00** |
| 5. ligne **en plein vol** (3 s sur 12,6 s) | **42,3176** — ni la référence, ni le réglage dès le pas 0 |
| 6. bus du **pilote**, neutre par socket | écart **0,000000e+00** |
| 7. bus du **pilote**, non neutre | 113,0068 → **148,9144** |

Les cas 3, 4 et 6 sont des **égalités exactes** (0,00e0), pas des tolérances. La
porte garantit l'ordre des cas 3 et 4 **par construction** (la ligne est envoyée
avant que le pilote ne se connecte, et le nœud n'accepte qu'après) : aucune course
de `sleep` n'est supposée.

**Trois défauts réels trouvés en écrivant cette porte, et corrigés :**

1. le bus du nœud était créé **après** `ecoute.accept()` — donc le serveur de bus
   n'écoutait pas encore quand la porte envoyait sa ligne (`ConnectionRefused`) :
   un bus qui ne s'ouvre qu'après la connexion ne peut pas moduler le premier pas ;
2. le gain d'une région **finale** est **absorbé par la normalisation de sortie**
   (113,0068 avec et sans `gain=2`,0) : le piège documenté de C5, retombé dedans —
   la porte module désormais un nœud du **milieu** ;
3. `LANCÉS=()` : un nom de **variable** accentué n'est pas un identifiant bash
   valide (les noms de *fonctions* accentués, eux, passent — d'où l'erreur tardive).

**Ce qui reste pour C5ter :** authentifier les modulateurs (aujourd'hui quiconque
atteint le port peut moduler — c'est signalé à l'écoute), et le **retour d'état** :
le modulateur ne sait pas ce que sa ligne a produit, seulement qu'elle est validée.

---

## C12bis — FAIT (9 octobre 23 h 05) : trace du nœud et fusion par le temps mural

**Ce qui manquait, et qui était grave.** Seul le PILOTE traçait (C12). Une divergence
sur un lien n'était donc visible que d'un bout : impossible de dire si c'est l'envoi
ou la réception qui avait dérivé. Et les traces de deux processus n'étaient pas
comparables — chacune avait ses propres durées locales (`ms`), donc aucun temps
commun pour les ordonner.

**Ce qui est fait :**

- le **nœud trace aussi**, sous les **mêmes noms de lien** que le pilote
  (`local->pair` pour ce qu'il reçoit, `pair->local` pour ce qu'il rend). C'est cette
  convention — et non une tolérance de temps — qui rend les deux bouts appariables :
  `(lien, pas, n)` suffit, sans seuil ni epsilon ;
- la trace passe en **v2** : `t_abs` (heure murale, epoch) et `mode` (0 dense, 1/2
  listes, 3/4 lots) s'ajoutent. Une v1 reste **lisible** ; elle n'a simplement pas
  d'horodatage, et la fusion **refuse alors de l'ordonner** ;
- `--fusionner-trace T1 T2 [...] [--fusion-sortie F]` : ordre **total et
  déterministe** (temps, puis source, puis pas, puis lien), **dérive d'horloges
  mesurée et non corrigée**, et **confrontation des deux bouts de chaque lien** —
  identiques / divergents / **non vérifiables** (un lien en mode listes est quantifié,
  deux empreintes différentes y sont normales : le déclarer « vérifié » serait
  mentir).

**La porte** (`tools/porte-fusion.sh`), quatre cas, exécution répartie réelle :

| cas | résultat |
|---|---|
| 1. trace des deux côtés | pilote **94** croisements · nœud **94** (source `d`) |
| 2. fusion | **188** croisements de 2 sources, ordonnés par le temps · **94 liens identiques, 0 divergents** · dérive d'horloge **+0,000 148 s** |
| 3. un bit changé chez le nœud | **`local->pair` pas 0 : DIVERGENT** — `…35e8` d'un côté, `…35e9` de l'autre · **code 3** |
| 4. trace v1 / trace seule | **refusées** (code 2), avec la raison : « l'ordonner par numéro de pas donnerait un faux ordre » |

**Un défaut trouvé par la porte elle-même** : le mode fusion rendait la main au lieu
de sortir, et le programme continuait vers le chargement du modèle (« ouverture du
GGUF: No such file ») **après** avoir imprimé une fusion juste. Corrigé, et c'est
exactement ce qu'une porte sert à attraper.

**Ce qui reste pour C12bis** : fusionner des traces **de plus de deux processus**
(le mode accepte déjà N fichiers, mais seule la chaîne à 2 régions est passée en
porte), et le cas où deux nœuds partagent un même nom de région (aujourd'hui refusé
comme ambigu).

---

## C4 (premier pas) — FAIT (9 octobre 21 h 55) : pas par région et borne explicite

**Ce que C4 demande** : que chaque région ait **son** horloge, sans horloge globale.
Le pas complet (asynchronisme réel) est un chantier de plusieurs semaines ; ce
premier pas livre ce qui se vérifie **aujourd'hui** et ce qui manquait pour
l'attaquer :

- **un compteur de pas par région** — la région locale et chaque nœud annoncent le
  nombre de pas qu'ils ont servis (`[horloge] 63 pas servis`) ;
- **`--pas-max N`** — une borne de terminaison. Si elle est atteinte, l'exécution
  **s'arrête et le dit**, et **aucune perplexité n'est rendue** : un chiffre calculé
  sur la moitié des jetons aurait l'air d'un résultat complet, et c'est précisément
  ce que le dépôt refuse.

**La porte** (`tools/porte-horloge.sh`), trois cas mesurés :

| cas | résultat | code |
|---|---|---|
| sans borne | 59,0790 · **63 pas servis** par région | 0 |
| borne = 64 (non atteinte) | **59,0790** (identique) · 63 pas servis (borne 64) | 0 |
| **borne = 32 (atteinte)** | **aucune perplexité rendue** · « L'exécution s'arrête ICI » | **5** |

**Ce qui reste pour C4, et c'est dit** : l'**asynchronisme réel** — des régions qui
avancent à leur propre rythme, avec des barrières seulement là où un calcul les exige.
Cela suppose que le jeton devienne un **événement horodaté** circulant dans le graphe,
donc C2 (entrées multiples) d'abord. Le compteur et la borne sont les deux
instruments qui rendront ce chantier mesurable.

---

## C5bis — FAIT (9 octobre 18 h 40) : diffusion du bus par FICHIER DE CONTRÔLE

**Livré** : `--bus-fichier F` sur un nœud. Le fichier est **relu avant chaque trame**,
donc un **autre processus** peut changer un canal **pendant l'exécution** — c'est ce
qui en fait un bus et non un réglage de démarrage. Le format est celui du module
(`MODULATION canal valeur`), et une ligne illisible est **refusée** (test unitaire).

**La porte** (`tools/porte-bus.sh`, cas 4), sur un nœud **relais** :

| fichier de contrôle | perplexité de la chaîne à trois régions |
|---|---:|
| sans canal | **59,0790** |
| `MODULATION gain 1.5` | **66,0379** ✅ — la région du milieu applique le canal diffusé |

**Deux leçons, tombées deux fois chacune — elles sont écrites pour de bon :**

1. **Le gain d'un nœud FINAL est invisible** : la normalisation de sortie divise par
   la norme, donc un facteur scalaire y disparaît. Tout test de bus doit viser une
   région du **milieu**. (Je suis retombé dans le piège avec le fichier de contrôle :
   premier essai sur un nœud final, résultat identique — et ce n'était pas le bus.)
2. **Une porte mal formée ressemble à une capacité cassée.** Le cas 4 a d'abord
   échoué parce que mon `printf '%s'` écrivait un `\n` **littéral** : la valeur devenait
   illisible, et le parseur la **refusait**. C'est le parseur qui avait raison.

**Ce qui reste pour C5** : le transport par **socket** (`--bus-serveur`, l'option est
posée et le parseur est prêt) demande que le fil d'écoute soit lancé **avant**
`ecoute.accept()` dans `run_serveur_flux` — un fil posé après n'écoute que pendant
qu'un client est connecté, et c'est exactement ce que j'ai mesuré : connexion
refusée. Le fichier de contrôle couvre le besoin en attendant.

---

## C3 — FAIT (9 octobre 18 h 20) : les délais par lien

**Livré** : la topologie déclare `delai_ms` par lien (C3a l'avait déjà dans le
format), et le moteur **l'applique** — le pilote sur son lien sortant, le **nœud
relais** sur le sien. L'invariant est le plus net du plan : **un délai change le
temps, jamais un chiffre**.

**La porte** (`tools/porte-delais.sh`), mesurée :

| cas | perplexité | empreintes | mur |
|---|---:|---|---:|
| délai 0 ms | 59,0790 | référence | 6,23 s |
| **délai 50 ms par trame** | **59,0790** (identique) | **identiques** (126 croisements, horodatage exclu) | **9,35 s (+3,1 s)** |

**3,1 s de plus = 50 ms × 64 pas** : le délai est bien appliqué, et il ne touche
**aucun** chiffre. C'est la trace (C12) qui le prouve, empreinte par empreinte — une
porte qui ne comparerait que la perplexité laisserait passer une modification de la
charge transportée.

**Ce que cela donne pour la suite** : la loi de coût des délais est maintenant dans
le moteur, et elle recoupe la mesure de la campagne (**3,4 ms par jeton et par ms de
RTT**, `docs/modele-pour-drave.md` § 8 bis). Un graphe de régions peut donc être
*conçu* avec ses délais, et leur prix se lit à l'avance.

---

## C5 — FAIT (9 octobre 19 h 10) : le bus de modulation multi-canaux

**Livré** : `drave-core/src/bus.rs` (5 tests) + `--bus canal=valeur` (répétable, sur
le pilote **et** sur les nœuds). Le bus porte des canaux nommés ; **chaque région
décide de ce qu'elle en fait** — c'est la définition biologique du neuromodulateur.
Premier consommateur câblé : le **gain de région**, appliqué à l'état que la région
produit. Valeur neutre par canal (`gain` = 1,0, les autres 0,0) : un canal absent ne
change rien, et c'est ce qui rend la porte vérifiable.

**La porte** (`tools/porte-bus.sh`), trois cas — et le troisième a demandé une
correction de protocole :

| cas | mesure |
|---|---|
| 1. bus **neutre** (`gain=1`) | perplexité **59,0790 = 59,0790** · **126 croisements, empreintes identiques** (horodatage exclu) ✅ |
| 2. bus **non neutre** (`gain=1,5`) | perplexité **64,1160** (elle change) · empreintes changent ✅ — le bus est **branché** |
| 3. bus sur un nœud **relais** (région du milieu) | **66,0379** contre **59,0790** sans bus ✅ — le bus **traverse les instances** |

**Ce que le cas 3 a appris** : le gain d'un nœud **final** est **absorbé par la
normalisation de sortie** (une norme divise par la norme : un facteur scalaire y
disparaît). C'est un nœud du **milieu** qui prouve que le bus agit — sa sortie
alimente une autre région, sans normalisation interposée. Le premier test était donc
faux, pas le bus.

**Ce qui reste pour C5, et c'est dit** : le transport du bus est **local à chaque
instance** (`--bus` sur chacun). La diffusion d'un canal par le **réseau** (message
de contrôle `MODULATION canal valeur`, dont le format est écrit dans `bus.rs`) reste
à câbler — c'est la prochaine étape de la capacité, pas son invariant.

---

## Prochaines étapes (dans l'ordre)

1. **C1b — pilote multi-régions** (conception ci-dessus) : une topologie **linéaire** à
   trois régions sur trois instances doit rendre la **même perplexité** que le modèle
   entier, et le cas à deux nœuds doit reproduire l'écart **0,00e0** d'aujourd'hui.
2. **C12 — trace globale** : chaque événement porte `(région, pas, lien, horodatage)`,
   et un mode `--rejouer-globale` doit rejouer l'exécution **à l'identique**.
3. **C5 — bus de modulation** : canaux (`recompense`, `nouveaute`, `incertitude`)
   diffusés à toutes les régions, y compris entre instances ; porte : canal nul ⇒
   aucune différence, bit à bit.

## Bilan du sprint (9 octobre, 19 h 20)

**Les trois capacités sont livrées avec leurs invariants vérifiés**, chacune par une
porte outillée et rejouable :

| capacité | module | porte | invariant mesuré |
|---|---|---|---|
| **C1** graphe de régions | `topologie.rs` | `tools/porte-topologie.sh` | graphe linéaire = découpage historique (**même chiffre**) · trois régions sur trois instances = référence (**écart 0,00e0**) · deux refus vérifiés |
| **C12** trace globale | `trace_globale.rs` | `tools/porte-trace.sh` | **126 croisements, aucune divergence** au rejeu · trace faussée d'un bit **détectée et nommée** |
| **C5** bus de modulation | `bus.rs` | `tools/porte-bus.sh` | bus neutre ⇒ **empreintes identiques** (126 croisements) · gain 1,5 ⇒ la sortie change · bus d'un nœud **relais** ⇒ agit à travers les instances |

**Tests : 95** (77 d'origine + 18 ajoutés) et **les 23 portes du dépôt sont
VERTES, 0 rouge** (`tools/portes.sh`, relancé à 17 h 46, terminé à 18 h 01, code 0).
Le relevé, pour mémoire :

```
cargo test --release                       95 verts  ✅      (77 avant le sprint)
gpt-oss-120b MXFP4 ctx 256                 15.6017  ✅      (la valeur attendue)
formats contre libggml                     17 concordent, 0 diverge  ✅
porte de correction (llama.cpp)            100 % des positions utiles ≥ 0,95  ✅
le rejeu de la trace                       écart 0.00e+00  ✅
découpage à deux nœuds, 5 modes            0.00e0 / 0.00e0 / 3.65e-2 / 0.00e0 / 4.45e-3  ✅
```

**Non-régression** : `porte-flux.sh` repassée après **chaque** modification du chemin
d'exécution — cinq modes verts — et la suite complète relancée en fin de sprint.

**Trois défauts trouvés par les portes, et c'est leur raison d'être** :

1. **fin de plage exclusive** — j'envoyais `derniere` au lieu de `derniere + 1` :
   la dernière couche de la région distante n'était plus exécutée, et **seuls les
   modes 0, 1 et 2** étaient touchés (3 et 4 passent par un autre encodeur) ;
2. **`--topologie` avalait `--ppl-reparti`** — la commande imprimait le plan au lieu
   de mesurer (arrivé deux fois : au pilote, puis au nœud relais) ;
3. **le gain d'un nœud final est absorbé par la normalisation de sortie** — le test
   du bus était faux, pas le bus ; c'est un nœud du **milieu** qui le prouve.

**Ce qui reste, et qui n'est pas dans le périmètre du sprint** : les entrées
multiples et la récurrence (**C2**), les délais et horloges (**C3**, **C4**), la
mémoire épisodique et la consolidation (**C6**, **C7**), la périphérie (**C8**), la
latéralité et les budgets (**C9**, **C10**) — et, pour C5, la **diffusion réseau** du
bus (le format de la ligne de contrôle est écrit, le transport reste à câbler).

---

## Journal du sprint

| heure | fait |
|---|---|
| 9/10 17 h 10 | **C1a** : module `topologie.rs`, validation stricte, plan, 8 tests, suite à 85 tests. |
| 9/10 17 h 20 | **C1b pas 1** : la topologie pilote le découpage · porte `tools/porte-topologie.sh` **TENUE** (même chiffre, écart 0,00e0) · deux refus vérifiés. |
| 11/10 04 h 30 | **LA ROUGE INSTRUITE ET CORRIGÉE — c'était la PORTE.** Le fichier a **255** jetons, la porte en annonçait 128 ; `--ppl` note les N **premiers**, `--ppl-reparti` les N **derniers** ⇒ elle comparait **deux textes différents**. Corrigé (jetons comptés) : dense **173,0196 = 173,0196** et routé idem, **écart 0,0000 %** ⇒ **notre modèle entraîné survit au découpage, routage compris**. **20/20 portes vertes.** |
| 11/10 03 h 00 | **VÉRIFICATION COMPLÈTE** : 20 portes jouées après les 8 rounds qui ont touché le chemin d'exécution ⇒ **19 vertes · 1 rouge** + 122 tests. La rouge est `porte-reparti-moteur` (notre modèle `/tmp/moteur_route.gguf`, entier 321,9623 contre réparti 132,8349, écart 58,7 %, **flux à 0,00e0**) : tous les ajouts du sprint sont INACTIFS par défaut sur ce chemin, donc elle est **pré-existante et non expliquée** — écrite comme telle, avec la commande pour l'instruire. |
| 11/10 01 h 30 | **C10 (suite) — budget de LATENCE** : `"budget_ms"`, comparé à l'allé-retour mesuré. Généreux ⇒ identique (111,9225, code 0) · 1 ms ⇒ `LATENCE DÉPASSÉE : 20,1 ms pour un budget de 1 ms, au pas 0`, **code 8**, aucune perplexité. **Quatre codes distincts** : 5 borne · 6 octets · 7 panne · 8 latence. Défaut de porte corrigé (variable `D` écrasée ⇒ code 127). |
| 11/10 00 h 30 | **C11 — pannes de lien** : `best-effort` = « sauter la région » est REFUSÉ (un graphe amputé est un AUTRE modèle) ⇒ s'arrêter en nommant lien/pas/octets, **code 7** (5 = borne, 6 = budget). Porte 3 cas : nominal 33,0156 · pair tué au pas 12 (43 968 octets) · pair absent en 2 s. Deux défauts corrigés : un pair absent faisait PANIQUER le pilote (code 134) ; la porte attendait un événement fragile. Reste : la REPRISE (cache KV perdu). |
| 10/10 23 h 00 | **C10 — budget d'octets par lien** : `"budget_octets"` dans la topologie, vérifié **sur ce qui passe** (la taille dépend de l'activité, pas du mode). Porte 3 cas : sans budget 111,9225 · budget généreux **identique** · budget insuffisant ⇒ arrêt **au pas 0**, lien/octets/budget nommés, **code 6**, **aucune perplexité**. |
| 10/10 22 h 00 | **C6 — clé de FENÊTRE : prédiction RÉFUTÉE.** W=1 : 50 (bon indice) et 1 006 (mauvais), séparation 1,31/64. W=4 : 653. W=16 : 573. **W=64 : 449 (= le hasard)** et **séparation 19,94/64**. Le lissage **détruit le bon indice** et **effondre la sélectivité** ⇒ troisième confirmation du §24 quater : **abstraire par moyennage détruit la rappelabilité** ; la sélectivité EST la netteté de la clé. ⇒ pour chercher par question : des **jetons** (RAG) ou une **clé apprise**, pas le contenu brut. |
| 10/10 20 h 45 | **C6 — le rappel n'est pas CONTINU** : six dernières positions prélevées une à une. `only` (4ᵉ) → **50 jetons**, `code` (5ᵉ) → **1 006** : **deux jetons voisins**, dont les états ont lu presque le même texte. Cause : la clé est un **k-WTA**, donc une petite variation fait entrer/sortir des canaux et la clé **saute** — aucune pente à suivre. Voie ouverte : clé formée sur une **FENÊTRE** de positions. |
| 10/10 19 h 30 | **C6 — le rappel dépend de l'INDICE** : 8 indices (positions 1..128 depuis la fin de B), distances **[50, 303, 303, 311, 347, 347, 890, 1003]**, moyenne 444, hasard 448. **Un indice trouve (50 jetons, 9× mieux que le hasard), sept sont au hasard** ⇒ le « 3,3× » du round 2 était un tirage chanceux, et **la limite est le CHOIX de l'indice**, pas la mémoire. `--etat-fin` accepte une liste de positions. |
| 10/10 18 h 00 | **C6/C2 — la mémoire QUI SERT (bout en bout)** : `--episodique-extraire`. Indexer A (1 750 états) → retrouver avec un indice extérieur (épisode 437, **303 jetons** de l'aiguille, hasard 448) → injecter dans une invite sans le fait : le modèle DIT **« The vault access code is »** (α=0 : `150px`, témoin). **Le code n'est pas produit** car l'épisode retrouvé précède l'aiguille ⇒ **le goulot est le RAPPEL, pas la greffe**. |
| 10/10 16 h 30 | **C2 — deux entrées, règle de mélange** : `porte-melange.sh` (4 cas, verte). La somme **arbitre** (7/7), **bascule à α=0,6** contre **0,509** prédit par les normes. Et **correction d'un faux négatif majeur** : la greffe d'état **transfère le contenu** (`ZQ3`/`K00`) quand l'état est capturé dans la numérotation de l'inférence (`--etat-fin` — le décalage d'un jeton faisait injecter l'état qui prédit « : »). Trois mesures avaient échoué sur ce décalage. |
| 10/10 14 h 10 | **C6 — indice étranger : la porte CORRIGE la mesure.** En écrivant la porte, la question a gagné un point d'interrogation : 136 → **378 jetons** (hasard 448). L'effet est réel mais **NON ROBUSTE** ; la porte n'exige plus que « mieux que le hasard » et **affiche l'avertissement** quand la marge est faible. Leçon : un chiffre unique sur un seul indice n'est pas un résultat. |
| 10/10 13 h 00 | **C6 — indice étranger** : `--episodique-indice` (état EXTÉRIEUR). Un indice pris dans le magasin s'y retrouve lui-même (64/64, 1 009 jetons de l'aiguille) et **ne teste rien** — piège corrigé. Avec un indice extérieur partageant **4/64** canaux : épisode rendu à **136 jetons** de l'aiguille contre **448** de hasard ⇒ **3,3× mieux que le hasard**, faible mais réel. Limite écrite : un seul indice, un seul texte. |
| 10/10 11 h 30 | **C2/C6 — la greffe d'état** : `--fusion-etat/pos/alpha` + prélèvement d'état multi-positions. Protocole A/B (même texte, l'aiguille en moins) : témoin poids 0 identique · A + son état garde son contenu · **B + l'état de A ne donne jamais le code** (5 poids, et même partout) · **cause** : le 1er jeton change, la suite reste celle de B (cache KV). ⇒ une mémoire doit entrer comme contenu ou entrée de cache ; **le moteur n'a aucune prise sur le KV — manque**. Trois pièges corrigés (défaut 0,0 du poids, position « dernier » comptée par le moteur, `DRAVE_DEBUG_FUSION` déclarée). Porte 5 cas. |
| 10/10 10 h 05 | **C7 suite — rejeu répété = point fixe** : du cycle 2 au cycle 12, mêmes prototypes, même compression, même rappel contre les épisodes d'origine, et erreur **exactement 0,00e0**. Rejouer une mémoire ne l'use pas. Cas 8 (`--episodique-cycles`). |
| 10/10 09 h 35 | **C6 suite — la mémoire localise** : erreur moyenne **en jetons** entre l'épisode rendu et l'interrogé. À N=300 : Δ=2 à 50 % de dégradation, 24 à 75 %. À **N=2 048** : Δ=**11 jetons à 50 %** (0,54 % du texte), 86 à 75 %, rappel 95,4 %, **round-trip 2 048/2 048**, élagage 81 %. La précision RELATIVE s'améliore avec la taille : quand la mémoire se trompe, elle se trompe de PRÈS. Cas 3bis dans `porte-episodique.sh`. |
| 10/10 09 h 00 | **C9 × C1 — où couper ?** Lien sans perte : **8 points de coupe, une seule perplexité (113,0068)**. Lien encodé : 8,9 % d'écart entre les coupes (108,87 à 118,53). Coût d'un pont de 448 fibres : **+0,52 % après 18 couches, +2,81 % après 12, +17,09 % après 15** — facteur 30 ⇒ **couper tard**. Porte 3 cas ; elle a attrapé son propre défaut (pont asymétrique, +4,92 % au lieu de +2,81 %). |
| 10/10 08 h 20 | **C8 (pas 1)** : le réflexe mesuré comme sortie précoce. `--reflexe-essai` : accord **0 % jusqu'à 16 couches sur 24**, 6,2 % à 20, **100 % à 24** (le réflexe EST le modèle). Cause mesurée : **cos(état tronqué, état final) = 0,044 / 0,145 / 1,000** à 1 / 16 / 24 couches — l'état intermédiaire est presque orthogonal au final, donc la tête de la dernière couche ne peut pas le lire. Gain de temps réel (18,5×). Manque écrit : une tête dédiée par profondeur. Porte 4 cas. |
| 10/10 07 h 00 | **C9/C10 (pas 1)** : pont à fibres limitées. Piège 1 : le pont ne limitait que l'aller (1 096 vs 1 959 octets) — corrigé, les deux sens reçoivent `--pont-k`. Piège 2 : en **dense f32 élaguer ne gagne aucun octet** (3 664 avant et après, +7,83 %). Courbe en blocs : 448 fibres → +2,81 % et ÷1,8 en octets ; 224 → +108,9 % (falaise). À budget égal, quantifier bat élaguer de 83 %. Porte 7 cas. |
| 10/10 05 h 20 | **C7 (pas 1)** : consolidation par rejeu (fusion des épisodes qui co-activent), deux formes de prototype. **L'exemplaire bat la moyenne partout** : seuil 1 → 7 % du magasin pour 87 % de rappel, contre 13 % pour 22 % ; seuil 8 → 51 % pour 95,3 % contre 67 % pour 34 %. Mécanisme : la clé d'une moyenne ne coïncide avec la clé d'aucun membre. Porte : cas 7. |
| 10/10 01 h 50 | **C6** (mémoire épisodique) : module + mode `--episodique-essai` sur états réels. Round-trip **300/300 au bit près** (aussi après disque) ; rappel 100/96,7/69,3/15,3 % selon dégradation ; nouveauté 41,5 vs 64. **Trois négatifs mesurés** : aucun élagage (300/300 candidats), l'espacement des états ne change rien (24,0 vs 23,9), et à k=8 **81 collisions ⇒ round-trip 219/300**. Décorrélation : rappel 50 % → 78,3 %, toujours 0 % d'élagage. Porte `porte-episodique.sh` (5 cas). |
| 10/10 00 h 20 | **C5ter** : bus par le réseau (`--bus-serveur`) sur le pilote et le nœud, protocole du fichier, borné à 8 modulateurs, verrou pris une fois par ligne. Porte 7 cas : socket ≡ statique et neutre ≡ référence **au bit près (0,00e0)**, plein vol ≠ les deux. Trois défauts corrigés : bus créé après `accept()`, gain d'une région finale absorbé par la normalisation, variable bash accentuée. |
| 9/10 23 h 05 | **C12bis** : le nœud trace (mêmes noms de lien), format v2 horodaté + mode, `--fusionner-trace` (ordre déterministe, dérive d'horloges mesurée, liens confrontés). Porte : 94/94 liens identiques ; **1 bit changé ⇒ DIVERGENT au pas nommé, code 3** ; v1 ⇒ refusée, code 2. 107 tests. Défaut attrapé par la porte : le mode fusion ne sortait pas et le moteur chargeait un modèle après coup. |
| 9/10 21 h 55 | **C4 (pas 1)** : compteur de pas par région + borne `--pas-max` · porte `tools/porte-horloge.sh` (même résultat sans borne et à borne 64 ; **arrêt explicite code 5 sans résultat partiel** à borne 32). |
| 9/10 18 h 40 | **C5bis** : bus diffusé par fichier de contrôle · cas 4 de `porte-bus.sh` vert (relais 66,0379 contre 59,0790) · deux leçons : le gain d'un nœud final est invisible, et une porte mal formée ressemble à une capacité cassée. |
| 9/10 18 h 20 | **C3** : délais par lien · porte `tools/porte-delais.sh` — **même perplexité (59,0790), empreintes identiques, +3,1 s pour 50 ms × 64 pas**. |
| 9/10 18 h 01 | **23 portes du dépôt : 23 vertes, 0 rouge** (code 0), dont `cargo test` à 95 verts et gpt-oss à 15,6017. |
| 9/10 19 h 20 | **Bilan** : trois capacités livrées, 95 tests, 23 portes vertes. |
| 9/10 19 h 10 | **C5** : bus de modulation · porte `tools/porte-bus.sh` (neutre ⇒ empreintes identiques · gain 1,5 ⇒ la sortie change · bus du relais ⇒ agit). 95 tests, porte-flux verte. |
| 9/10 18 h 40 | **C12** : trace globale + rejeu · porte `tools/porte-trace.sh` (126 croisements, aucune divergence ; trace faussée détectée au bit près). 90 tests. |
| 9/10 18 h 00 | **C1b pas 2** : le RELAIS · trois régions sur trois instances, **écart 0,00e0**, même chiffre que deux régions. **Bug de fin de plage exclusive trouvé et corrigé** — attrapé par `porte-flux.sh` (modes 0, 1, 2 cassés, réparés : 0.00e0 / 0.00e0 / 3.65e-2). |
