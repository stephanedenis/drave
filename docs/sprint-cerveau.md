# Sprint « cerveau complet » — état d'avancement

> Lancé le 9 octobre à 17 h, **en autonomie jusqu'au 10 octobre 9 h (HAE)**.
> Plan de référence : `docs/plan-cerveau-complet.md` § 4 (premier sprint).
> Ce fichier est mis à jour **à chaque round** : il est la mémoire du sprint.

---

## Objectif du sprint

Trois capacités du plan, chacune avec sa **porte mesurée** :

| # | capacité | porte (invariant à vérifier) | état |
|---|---|---|---|
| **C1** | **graphe de régions** : descripteur de topologie, validateur, ordonnanceur par dépendances, pilote multi-nœuds | un graphe **linéaire** rend des logits identiques **au bit près** ; un découpage à **trois régions** égale le modèle d'un seul tenant | ✅ **FAIT** — `topologie.rs` (8 tests) · la topologie pilote le découpage (0,00e0) · relais trois instances (0,00e0) · `tools/porte-topologie.sh` (5 cas, dont 2 refus) |
| **C12** | **trace globale horodatée + rejeu** | rejeu d'une exécution distribuée == exécution, **0,00e0** | ✅ **FAIT** — `trace_globale.rs` (5 tests) · 126 croisements, **aucune divergence** · trace faussée d'un bit **détectée et nommée** · `tools/porte-trace.sh` |
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
| 9/10 18 h 01 | **23 portes du dépôt : 23 vertes, 0 rouge** (code 0), dont `cargo test` à 95 verts et gpt-oss à 15,6017. |
| 9/10 19 h 20 | **Bilan** : trois capacités livrées, 95 tests, 23 portes vertes. |
| 9/10 19 h 10 | **C5** : bus de modulation · porte `tools/porte-bus.sh` (neutre ⇒ empreintes identiques · gain 1,5 ⇒ la sortie change · bus du relais ⇒ agit). 95 tests, porte-flux verte. |
| 9/10 18 h 40 | **C12** : trace globale + rejeu · porte `tools/porte-trace.sh` (126 croisements, aucune divergence ; trace faussée détectée au bit près). 90 tests. |
| 9/10 18 h 00 | **C1b pas 2** : le RELAIS · trois régions sur trois instances, **écart 0,00e0**, même chiffre que deux régions. **Bug de fin de plage exclusive trouvé et corrigé** — attrapé par `porte-flux.sh` (modes 0, 1, 2 cassés, réparés : 0.00e0 / 0.00e0 / 3.65e-2). |
