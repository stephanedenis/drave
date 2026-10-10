# Sprint « cerveau complet » — état d'avancement

> Lancé le 9 octobre à 17 h, **en autonomie jusqu'au 10 octobre 9 h (HAE)**.
> Plan de référence : `docs/plan-cerveau-complet.md` § 4 (premier sprint).
> Ce fichier est mis à jour **à chaque round** : il est la mémoire du sprint.

---

## ▶ PROCHAINE ACTION (à lire en premier)

État au **10 octobre 6 h** : **C1, C3, C4 (pas 1), C5, C5bis, C5ter, C6, C7 (pas 1),
C12, C12bis** livrées et poussées · **122 tests verts** · portes `porte-topologie`,
`porte-trace`, `porte-fusion`, `porte-bus`, `porte-bus-socket`, `porte-delais`,
`porte-horloge`, `porte-flux`, `porte-episodique` vertes.

**La consigne tient toujours : ne pas s'arrêter faute de liste.** Le temps imparti
(10 octobre 9 h) est un plancher, pas un plafond ; quand il tombe, la question n'est
pas « ai-je fini ? » mais « qu'est-ce qui est mesurable maintenant ? ».

**Ce qui vient d'être fait (contexte pour reprendre) :**

- **C6** : mémoire épisodique (clé k-WTA + index inversé). Trois négatifs mesurés
  d'abord (aucun élagage · l'espacement ne change rien · collisions à petit k), puis
  **trois ingrédients** pour que l'index élude : expansion (896 → 16 384), décorrélation,
  **égalisation d'usage des canaux** → élagage **83 %**, rappel 96,3 % à 50 % de
  dégradation, round-trip **exact au bit près** (300/300, 2 500/2 500, et sur 3 corpus).
  Coût d'expansion **fixe** ⇒ rentable au-delà de **N ≈ 2 048** épisodes.
- **C7 (pas 1)** : consolidation par rejeu (fusion des épisodes qui co-activent).
  **L'exemplaire bat la moyenne partout** (7 % du magasin → 87 % de rappel, contre
  13 % → 22 %) : la clé d'une moyenne ne coïncide avec la clé d'aucun membre.

**Par ordre de valeur mesurable :**

1. **C10 / C9 — le budget de FIBRES du pont** (en cours) : combien de canaux faut-il
   échanger entre deux régions pour ne rien perdre ? `--pont-k K` ne garde que les K
   plus grandes amplitudes de l'état échangé ; porte : `K = 0` (pont entier) doit être
   **bit à bit** identique au mode sans pont, et la courbe perplexité ↔ K (donc ↔ octets
   par pas) doit être monotone. C'est la question du corps calleux, et elle a une
   réponse utile pour la distribution sur lien lent.
2. **C2 — entrées multiples** (le plus lourd, à cadrer honnêtement) : exige deux plages
   de couches disjointes par processus ; aujourd'hui explicitement refusé. C'est le
   préalable de C8 (périphérie) et de C9 (jumelage).
3. **C8 — périphérie** : région d'entrée à horloge propre, région de sortie (effecteur
   avec délai), et **réflexes** (un lien qui court-circuite le centre). Invariant : une
   entrée constante produit une sortie constante.
4. **C7 suite** — consolidation **itérative** (plusieurs cycles de rejeu) : le rappel
   d'appartenance tient-il après 2, 4, 8 cycles ? Et le rejeu vers les **poids**, qui
   reste le vrai C7 : le moteur n'entraîne pas, les règles locales existantes sont
   mesurées **dégradantes** (8,8246 contre 8,3869) — il faut donc une autre règle, et
   c'est un chantier, pas une case à cocher.
5. **C6 suite** — la mémoire qui **sert** : retrouver un passage pertinent dans un
   document long et le réinjecter (protocole « aiguille » de `tools/aiguille.py`,
   18/18 jusqu'à 12 288 jetons sans mémoire) ; mesure : le rappel par contenu
   localise-t-il l'aiguille ?
6. **Modèles** (`docs/modele-pour-drave.md`) : designs H (routage en profondeur),
   I (budget d'événements appris), J (entraînement conscient de la quantification).
7. **Biologie** : E2 (croissance des connexions), E4 (équilibre E/I), E5 (rejeu).

**Trappes à ne pas retomber dans :**

- le gain de bus sur une région **finale** est absorbé par la normalisation de sortie —
  mesurer sur une région du **milieu** ;
- un nom de **variable** bash accentué n'est pas un identifiant valide (les noms de
  *fonctions* accentués passent) ;
- `pkill -f "<nom>"` se tue lui-même ; repérer les fils par PID ou par `flock` ;
- un nœud refuse une plage d'une seule couche (`f.debut >= f.fin`) ;
- `--depuis` gonfle les compteurs cumulés de paires ; `--limit` change le protocole
  de fenêtres ; un drapeau inconnu est **ignoré en silence** (utiliser
  `--options-strict` dans les scripts) ;
- deux lecteurs lourds concurrents font tomber le disque à 8,6 Mo/s : **sérialiser**.

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
