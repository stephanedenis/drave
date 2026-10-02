# Cohérence des `docs/` avec la vision Drave — révision du 02/10

**En une ligne** : les **18 documents** de `docs/` (4 870 lignes) ont été relus par
**cinq relectures adverses** puis corrigés un par un — **88 sites de correction**
dans `docs/` (95 avec `REPRISE.md`, comptés dans le diff), plus une **sixième
relecture adverse du diff lui-même**, qui a trouvé 13 défauts de plus (dont un
faux que j'avais introduit) ; le verdict est que **la
vision est tenue partout, mais qu'elle était muette dans quatre documents** (le
format, le transport, les grappes et le découpage en clusters ne disaient nulle
part qu'ils servent à *router des flux sur des grappes réparties* ni à *lire ces
flux pour adapter l'architecture*) — c'est la seule incohérence **de fond**
trouvée, et elle est corrigée. Le reste est de la **péremption datée** : des
chiffres ou des états de statut qui décrivaient l'état d'hier et contredisaient le
code d'aujourd'hui.

## 1. Méthode

| étape | ce qui a été fait |
|---|---|
| 1. cadrage | la vision retenue est celle de `docs/vision.md` **et** la précision du 02/10 : Drave ≠ llama.cpp ; listes d'activation (deux listes trinaires **ou** connexions pondérées) routées sur des **grappes de neurones** réparties entre composants et machines ; les flux sont aussi l'**instrument de débogage et d'analyse** qui adapte l'architecture à la tâche. llama.cpp n'est qu'une **porte de correction**. |
| 2. relecture | cinq relectures adverses en parallèle (A : vision/roadmap/programme/sprints/histoire · B : format-flux/format-clusters/convertisseur/colab-reparti/contexte-long · C : plan-modeles-lourds/gpu-topk/mla-vision/prefill-reparti · D : plan-mode4/plan-v4-flash/plan41/comparaison-spiking). Chacune devait citer `fichier:ligne`, la citation exacte, le problème et une correction minimale, **sans toucher aux fichiers**. |
| 3. correction | appliquée **par moi**, une assertion par remplacement (aucun remplacement silencieux : chaque ancre devait apparaître exactement une fois). |
| 4. contrôle | une sixième relecture adverse du **diff** (voir ci-dessous) ; les portes du dépôt relancées sur le binaire reconstruit. |

Aucun des correctifs ne change un chiffre **mesuré** : ils alignent le document
sur la mesure, ou datent une phrase qui ne l'était pas. **Aucune optimisation n'a
changé une sortie** : les seules corrections de code sont dans `model.rs` et
`tools/portes.sh` (§4) et l'une d'elles **change un verdict affiché** — c'est
précisément son objet.

### Ce que la relecture du diff a rattrapé (13 défauts de plus)

Relire son propre travail avec la même exigence que celui des autres paie : la
sixième relecture a trouvé, dans **mes** corrections, un faux (« `--config`
affiche *puits appris sur 36/36* » — `--config` ne charge pas le modèle, il répond
seulement « calculable : oui » ; c'est le **chargement** qui affiche la ligne),
un renvoi de ligne cassé **par ma propre insertion** (`format-clusters.md:176`
devenu `:181`), un « au jeton 7 » quand le rapport dit **position 3**, un
« ces trois propriétés » resté après l'ajout d'une quatrième, une politique YaRN
périmée dans `REPRISE.md` (bascule à **4 ×**, pas 1×), un `axe 3` là où il fallait
`axes 2-3`, un **19ᵉ format lisible** (`Q4_1`, lu par la même branche que `Q4_0`)
que mon décompte ignorait, et une affirmation « identique à l'original » pour les
clusters que **rien ne mesure** (la mesure documentée est `origine 15,2789 ·
clusters 15,2789`). Elle a aussi confirmé, en scannant les **28 en-têtes GGUF** du
parc, qu'**aucun verdict de calculabilité ne bascule à tort** après le correctif
`attn_sinks`, et relevé une **réserve latente** désormais écrite dans le code :
`attn_mla` ne consomme pas `lay.sinks`.

## 2. Le verdict, document par document

| document | verdict | ce qui a changé |
|---|---|---|
| `vision.md` | **cohérent, 15 sites** | gpt-oss 15,6017 ; « protocole v5, 5 modes » ; « lot en listes » n'est plus rangé dans les manques ; l'axe 3 ne dit plus « rien » (il y a le transport et les grappes) ; deux paragraphes ajoutés sur les deux cas d'encodage (**trinaire deux listes** / **connexions pondérées**) et sur la lecture des flux pour adapter l'architecture ; sources ajoutées aux tableaux de mesures |
| `roadmap.md` | **cohérent, 6 sites** | mêmes valeurs de porte, renvois de sources |
| `programme-recherche.md` | **cohérent, 4 sites** | 4ᵉ propriété structurelle « **le flux se route** » ; 5,3 G événements/s sourcé |
| `sprints.md` | **cohérent, 1 site** | les portes citées sont celles de `tools/portes.sh` |
| `histoire.md` | **cohérent** | rien à changer (le renommage et la chronologie tiennent) |
| `format-flux.md` | **corrigé, 4 sites** | le format sert **quatre** choses : trace, rejeu, transport, **analyse** ; le critère de coût du mode 4 est daté (« à 256 jetons : 5,6× à 20 jetons ») |
| `format-clusters.md` | **corrigé, 1 site** | les grappes sont **le mécanisme de placement** (neurones répartis, flux routé de l'une à l'autre), pas un rangement de fichiers |
| `colab-reparti.md` | **corrigé, 2 sites** | en-tête **v5** ; le flux transporté est aussi **le journal** qu'on relit pour adapter l'architecture |
| `convertisseur.md` | **corrigé, 7 sites** | « Ordre de marche » remis à l'état réel (mmap, NUMA, Q8_0, routeur MoE, lecteur Q4_K/Q6_K étaient **faits**) ; hypothèses « suspects restants » remplacées par ce qui a été **testé le jour même** ; conteneur renommé (ex-`QTNT`) ; « calque » → « couche » |
| `contexte-long.md` | **corrigé, 5 sites** | E1 mesuré (−20 % / −31 %) ; E2 et E3 aux valeurs **par bloc de 32** ; **E6 MLA « non testable » → validée** ; **E7 vision « non testable » → faite** ; seuil YaRN à **4 ×** ; aiguille v2 **12/12** ; provenance des 234,88 |
| `plan-modeles-lourds.md` | **corrigé, 7 sites** | bandeau de statut, état d'arrivée des modèles, architectures `deepseek2`/`glm-dsa`, porte de flux |
| `plan-gpu-topk.md` | **corrigé, 4 sites** | cadrage axe 2, provenance du 234,88, 15,6017, 48 tests (49 depuis l'ajout du test d'identité paire/événement) |
| `plan-mla-vision.md` | **corrigé, 5 sites** | en-tête « non commencé » → **fait**, réserve du chemin dense, modèles MLA réellement présents |
| `plan-prefill-reparti.md` | **corrigé, 1 site** | le corps garde le plan historique à 39 octets, un bandeau dit que l'en-tête en fait **79** depuis la v4 |
| `plan-mode4-lot-listes.md` | **corrigé, 6 sites** | le document n'est plus « la spécification à implémenter » mais **la référence de conception d'une implémentation faite** ; protocole **v5, modes 0–4** ; durcissement fait ; message « mode 4 non écrit » disparu |
| `plan-deepseek-v4-flash.md` | **corrigé, 11 sites** | bandeau : lecteur multi-shards **fait**, V4.1-Flash a un **GGUF Q2** (365,71 Go), MLA **faite** ; gpt-oss = 128 experts **top-4** (et non top-8) ; étape 6 ajoutée (grappes + `--ppl-reparti`) |
| `plan-deepseek41-complet.md` | **corrigé, 5 sites** | MLA « validée à la **position 0** » (l'écart croît ensuite) ; types réels du fichier (dont **I8**, aucun I32) ; porte gpt-oss ajoutée aux portes vertes ; « aucun chiffre **de calcul** » |
| `comparaison-spiking.md` | **corrigé, 4 sites** | encadré : le spike est un **moyen** d'obtenir la parcimonie, le cœur de Drave (grappes + lecture des flux) n'est pas en cause ; sources internes citées ; 8,3 nJ **projeté** ; densité mesurée **17,9 %** sous le croisement de 22 % |

`REPRISE.md` (racine, hors `docs/`) a reçu **7 sites** du même ordre : un bloc de
portes à jour (**c'est lui qui fait foi**) en tête de §2, la ligne gpt-oss du
tableau des références, la commande de la porte gpt-oss, et trois mentions du
seuil YaRN resté à « 1,25 × » au lieu de **4 ×**.

## 3. L'incohérence de fond : la vision était muette là où elle devait être dite

C'est le seul point qui n'est pas de la péremption, et c'est celui qui répond à la
demande. Quatre documents décrivaient des **mécanismes** sans jamais dire à quoi
ils servent dans l'architecture du projet :

| où | ce qui manquait | ce qui a été ajouté |
|---|---|---|
| `format-flux.md` | le format servait trace, rejeu, transport — la **quatrième** finalité (lire les flux pour comprendre et adapter) était absente, alors que les outils existent (`tools/analyse_flux.py`, `profil_flux.py`, `diff_flux.py`) | « 4. l'**analyse** : les mêmes octets […] disent quels neurones travaillent — la donnée qui adapte l'architecture à la tâche » |
| `colab-reparti.md` | le transport était cadré comme une pure recette de fidélité | « Ce flux est aussi le **journal** qu'on relit […] pour comprendre où travaille le modèle et adapter l'architecture à la tâche » |
| `format-clusters.md` | les grappes étaient un **rangement de fichiers** et un gain de chargement | « **Et c'est le mécanisme de placement** : ces grappes sont les neurones qu'on répartit entre nœuds, et le flux d'activation se route de l'une à l'autre » |
| `comparaison-spiking.md` | le spike était présenté comme la cible | encadré : le cœur (router des flux sur des grappes réparties, lire ces flux) n'est pas remis en cause ; le spike est un moyen d'obtenir la parcimonie |

Deux documents ont aussi gagné la formulation explicite des **deux cas
d'encodage** que la vision distingue (`vision.md`) : la **liste trinaire en deux
listes** (le signe est porté par l'appartenance) et le **cas général en connexions
pondérées** par source. C'était implicite dans le code, pas dans le texte.

## 4. Ce que la relecture a trouvé **dans le code** (et qui a été corrigé)

Deux constats sont sortis des audits alors qu'ils n'étaient pas documentaires :

1. **`--config` refusait un modèle que le moteur calcule.** `manques_architecture`
   rangeait tout tenseur `attn_sinks` dans le manque « attention V4 : dé-rotation
   de sortie et puits par tête ». Or les puits appris **sont** implémentés
   (`attn_sinks.weight` est lu, `[config]` affiche « puits appris sur 36/36 ») :
   `drave gpt-oss-120b-MXFP4.gguf --config` répondait donc
   « **calculable : NON — il manque : attention V4…** » pour un modèle dont la
   porte (15,6017) tourne. Les deux causes sont maintenant séparées :
   `attn_derope` reste un manque, `attn_sinks` non. **Vérifié après correction** :
   gpt-oss → « calculable : oui » ; V4.1 → « calculable : NON — il manque :
   hyper-connexions, projection de sortie à rang faible groupée, attentions
   compressées CSA/HCA » (la liste exacte) ; V4-Flash → hyper-connexions et
   sortie à rang faible. C'est la **porte P0 du plan V4.1** (« `--config` annonce
   la bonne liste de manques ») qui est franchie pour les modèles du parc.
2. **Le message MLA surestimait sa validation** (« validée contre llama.cpp :
   corrélation 0,999024, top-1 3/3 ») alors que la validation s'arrête à la
   **position 0** et que l'écart croît ensuite (+0,009 / +0,372 / +0,611 puis
   **+4,070 nat** à la position 3). Le message le dit maintenant.

## 5. Ce qui reste ouvert

**Points à trancher par l'humain** (aucun n'est bloquant) :

1. **Séries KV canoniques** : `contexte-long.md` porte encore côte à côte les
   mesures « échelle par vecteur » (historique) et « par bloc de 32 » (courante).
   Le tableau E a été mis à la série courante ; il reste à décider si la série
   historique doit sortir du document ou rester comme trace datée.
2. **Porte gpt-oss de plein droit** : elle est désormais **exécutée** par
   `tools/portes.sh` (section 7 : `--config` puis la perplexité si les
   identifiants sont disponibles, ~20 min, hors mode `rapide`) — et elle est
   verte (15,6017, mesurée ce soir par le script). Sa valeur
   (15,6017) n'est **pas validée à l'extérieur** : llama.cpp applique YaRN dès la
   première position (166,85) là où nous le différons (15,6017), et en le forçant
   nous obtenons 84,07 — l'écart est du même ordre que celui du YaRN, ce qui
   encadre le chiffre sans le valider.
3. **`plan-deepseek-v4-flash.md`** : conservé comme trace datée avec un bandeau
   d'état en tête. Si tu préfères, il peut être fusionné dans
   `plan-deepseek41-complet.md` (V4-Flash y est le banc).
4. **DRVF et les deux cas d'encodage** : le format de flux transporte des listes
   quantifiées, pas encore la **connexion pondérée** ni la **paire de listes
   trinaires** telles que la vision les décrit. Est-ce que le format doit les
   spécifier maintenant, ou est-ce que c'est le chantier des hyper-connexions qui
   les fera entrer ?
5. **V4.1-Flash-Q2 est-il complet ?** Le fichier déclare `hc_mult = 4` mais ne
   contient aucun `output_hc_fn/base/scale`. Question de **provenance**, pas de
   code — elle commande la phase P7 du plan et peut invalider une partie du
   chantier. Rien ne permet d'y répondre depuis cette machine.
6. **19 formats lisibles, 17 à la porte** : `README.md` le dit maintenant
   explicitement (`Q4_1` et `Q5_1` sont lus par les mêmes branches que leurs
   voisins, mais ne sont pas dans la batterie comparée à libggml). Faut-il les
   **ajouter à la porte** ? Il suffit de deux lignes dans `tools/portes_formats.sh`
   si un GGUF du parc en contient un bloc.

## 6. Réserves de méthode

- Ces corrections sont **documentaires** : elles alignent le texte sur des mesures
  déjà publiées dans `reports/`. Aucune n'a produit de mesure nouvelle, sauf les
  deux vérifications de `--config` (§4) et la campagne de portes relancée.
- Les relectures adverses n'ont pas eu accès aux fichiers de modèles pour
  revérifier les perplexités elles-mêmes ; elles se sont appuyées sur les rapports
  et le code. La campagne de portes est là pour ça, et elle est **verte** :
  `cargo test --release` **48**, Qwen **19,3885**, clusters **799,8557**,
  formats **17 concordants / 0 divergence / 0 absent**, les **quatre** conventions
  de routage conformes au GGUF, et — nouveauté de ce soir — la porte **gpt-oss
  exécutée par le script** (`tools/portes.sh` section 7) : `--config` la dit
  **calculable** et la perplexité ctx 256 rend **15,6017**. Le binaire final
  (commentaires seuls après cette campagne) repasse les portes rapides.
- `journal/README.md` est régénéré par un hook : il apparaît modifié dans
  `git status` sans qu'une main l'ait touché, c'est normal.
- Les deux audits antérieurs (`rapport-coherence-docs.md`,
  `rapport-coherence-docs-2.md`) portaient sur la **cohérence avec le code** ;
  celui-ci porte sur la **cohérence avec la vision**. Les deux se complètent, ils
  ne se remplacent pas.
