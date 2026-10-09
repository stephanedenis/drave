# Sprint « cerveau complet » — état d'avancement

> Lancé le 9 octobre à 17 h, **en autonomie jusqu'au 10 octobre 9 h (HAE)**.
> Plan de référence : `docs/plan-cerveau-complet.md` § 4 (premier sprint).
> Ce fichier est mis à jour **à chaque round** : il est la mémoire du sprint.

---

## Objectif du sprint

Trois capacités du plan, chacune avec sa **porte mesurée** :

| # | capacité | porte (invariant à vérifier) | état |
|---|---|---|---|
| **C1** | **graphe de régions** : descripteur de topologie, validateur, ordonnanceur par dépendances, pilote multi-nœuds | un graphe **linéaire** rend des logits identiques **au bit près** ; un découpage à **trois régions** égale le modèle d'un seul tenant | **C1a FAIT** · C1b à faire |
| **C12** | **trace globale horodatée + rejeu** | rejeu d'une exécution distribuée == exécution, **0,00e0** | à faire |
| **C5** | **bus de modulation multi-canaux** | canal nul ⇒ sortie **inchangée** | mécanique partielle (fichier), bus à faire |

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

## C1b pas 2 — le relais : la conception, relevée sur le code

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

## Prochaines étapes (dans l'ordre)

1. **C1b — pilote multi-régions** (conception ci-dessus) : une topologie **linéaire** à
   trois régions sur trois instances doit rendre la **même perplexité** que le modèle
   entier, et le cas à deux nœuds doit reproduire l'écart **0,00e0** d'aujourd'hui.
2. **C12 — trace globale** : chaque événement porte `(région, pas, lien, horodatage)`,
   et un mode `--rejouer-globale` doit rejouer l'exécution **à l'identique**.
3. **C5 — bus de modulation** : canaux (`recompense`, `nouveaute`, `incertitude`)
   diffusés à toutes les régions, y compris entre instances ; porte : canal nul ⇒
   aucune différence, bit à bit.

## Journal du sprint

| heure | fait |
|---|---|
| 9/10 17 h 10 | **C1a** : module `topologie.rs`, validation stricte, plan, 8 tests, suite à 85 tests. |
| 9/10 17 h 20 | **C1b pas 1** : la topologie pilote le découpage · porte `tools/porte-topologie.sh` **TENUE** (même chiffre, écart 0,00e0) · deux refus vérifiés. |
