# 4. Le moteur Drave : exécution, structures, outils

> **Famille 4 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

---

## 4. Le moteur Drave : exécution, structures, outils

**Accumulateur** — Vecteur de sortie dans lequel le mode « push » disperse les
contributions : `acc[destination] += valeur × poids`. Sa taille décide de tout :
4 096 sorties × 3 octets = 12 Kio tiennent dans les blocs mémoire du FPGA, mais un
accumulateur par fil de calcul fait 36 Mo pour une tête de 151 936 sorties
(`reports/rapport-cpu-aer.md:11`, `reports/rapport-inference.md:131`).

**AER (Address Event Representation ; représentation par adresses d'événements)** —
Principe venu du matériel neuromorphique : une activation ne se lit pas dans un
tableau, elle est **poussée** vers ses destinations sous forme d'événements
(adresse + valeur). C'est l'origine du « push » du projet
(`docs/vision.md:29-36`, `reports/rapport-cpu-aer.md`). **Réf.** : Lazzaro,
Wawrzynek, Mahowald, Sivilotti & Gillespie, *Silicon auditory processors as
computer peripherals*, IEEE Transactions on Neural Networks 4(3), 1993 — cité sans
lien.

**Aiguillage (dispatch)** — Choix du noyau selon le format du tenseur (Q4_0, Q8_0,
MXFP4, i-quant…), qui remplace un appel unique `matvec_q4`. Il évite de convertir
et rend la lecture « en place » possible (`reports/rapport-mla-experts.md:98-99`).

**Binaire `drave` · crate `drave-core`** — Le moteur est un unique binaire Rust,
sans dépendance externe (`std` seul), construit par `cargo build --release` dans
`drave-core/`. Tous les bancs, mesures et bancs d'essai du dépôt l'appellent :
`drave <modele.gguf> --ppl`, `--infer`, `--plan`, `--flux-serveur`…
(`docs/colab-reparti.md:88-101`, `reports/rapport-inference.md:3-5`).

**Charge · `Flux` · `ChargeFlux`** — Structures internes du protocole :
`ChargeFlux::Dense(Vec<f32>)` porte un vecteur, `ChargeFlux::Liste(...)` une liste
quantifiée, `ChargeFlux::Lot(Vec<f32>)` un lot d'états aplati. `plat()` rend le
vecteur plat d'un lot ; `en_dense()` panique nommément sur un lot, pour qu'on
n'appelle pas la mauvaise conversion (`drave-core/src/main.rs`,
`docs/plan-prefill-reparti.md:116-126`).

**DenseQ4 · DenseQ8** — Les deux noyaux denses du moteur : `DenseQ8` lit un bloc
int8 à échelle par bloc de 32 et calcule un produit scalaire entier (exact au bit
près en AVX2) ; `DenseQ4` fait de même sur des nibbles signés biaisés, avec une
échelle `u16` par bloc (`docs/contexte-long.md:378-382`,
`reports/rapport-mur-memoire-4bits.md:87-92`).

**Dispersion (scatter)** — Écriture non contiguë : au lieu de lire une ligne de
poids, on écrit une contribution à une destination arbitraire. C'est le geste
central du push ; le GPU en fait 18,1 G événements/s et la DDR3 du FPGA en fait le
goulot (`reports/bilan-multi-materiel.md:39`, `:48`).

**Événement** — Dans ce dépôt, un événement est un **couple (écart d'indice,
valeur)** représentant une connexion active, sur 2 octets ; c'est l'unité de débit
du projet (« 5,3 G événements/s »). Ne pas confondre avec l'événement au sens
protocole réseau (`reports/bilan-multi-materiel.md:13`,
`reports/rapport-cpu-aer.md:5-9`).

**`forward` · `forward_lot` · `forward_mla` · `logits_lot`** — Les trois passes
avant du moteur : `forward` traite un jeton, `forward_lot` un lot d'états (mode 3
et 4), `forward_mla` le chemin d'attention latente. `logits_lot` note un lot
entier. Toute la phase 3 (transport) repose sur `forward_lot` et sur la règle que
la **norme finale** n'est appliquée qu'une fois, par le nœud qui a la tête
(`docs/plan-prefill-reparti.md:199-243`, `docs/roadmap.md:236-249`).

**FusedSign** — Structure de liste « une seule liste triée par destination + un
plan de signe » : elle fusionne les deux listes du cas trinaire en une seule, ce
qui économise la valeur à stocker (`drave-core/src/list.rs:187`,
`reports/rapport-optimisations.md:32`).

**Gather (lecture indexée)** — Lire les activations à des indices arbitraires, ce
que fait tout produit matrice-vecteur classique. Le mode push le supprime : chaque
source active connaît déjà ses lecteurs (`reports/rapport-cpu-aer.md:5`).

**Grappe (cluster)** — Groupe de neurones ou d'experts traité comme une unité de
chargement et de placement. « Le moteur ne répartit pas des matrices, il route des
listes » : une grappe est ce qu'on place sur un composant ou une machine
(`docs/format-clusters.md:1-11`, `docs/programme-recherche.md:39-46`).

**Greffon** — Un neurone ajouté à une couche **sans réentraînement**, à la forme
SwiGLU, chargé par `--patch`. Mesure : les neurones croisés n'apportent rien
(23,6125 → 23,6253), mais la plomberie d'apprentissage existe
(`reports/rapport-greffon.md:12-42`, `docs/programme-recherche.md:143-152`).

**Liste valuée · liste d'activation · liste creuse** — Le cœur de la
représentation : pour une couche et un jeton, la liste des neurones actifs, chacun
avec son indice, sa valeur et une échelle. « Une activation est un fait — "le
neurone 2 539 de la couche 23 a valu 27,8" — et non une case dans un tableau »
(`docs/vision.md:21-32`). **Où** : `drave-core/src/list.rs`, `DRVF`, `SparseVec`.

**`matvec` · GEMM · GEMV** — *GEMV* : produit matrice-vecteur (un jeton à la fois) ;
*GEMM* : produit matrice-matrice (plusieurs jetons ensemble, donc les poids relus
une fois pour tout le lot). Le préremplissage par lots est le passage GEMV → GEMM :
−20 % à −31 % de temps mesuré (`docs/contexte-long.md:52-59`,
`reports/rapport-prefill-par-lots.md`).

**Mode push · pull · auto · `seuil_push`** — *Push* : exécution par listes
d'événements dispersées dans un accumulateur. *Pull* : produit scalaire dense, qui
lit toute la ligne de poids. *Auto* : le moteur choisit d'après la densité
d'activation mesurée, avec un seuil `seuil_push = 0,22`
(`reports/rapport-croisement-push-pull.md:43-48`,
`reports/rapport-localite-activation.md:24`). **Où** : `--push`, `--dense`, `--auto`.

**Paire (indice, valeur) · paire (destination, valeur)** — L'unité de contenu d'une
liste : un indice (le neurone ou la destination) et une valeur quantifiée. Le mode 2
du protocole compte `n` **paires** ; le mode 4 compte des **états**, et le nombre
d'actifs d'un lot est `Σ a_j` (`docs/format-flux.md:110-116`,
`docs/plan-mode4-lot-listes.md:393-396`).

**Pool de threads · barrière** — Le moteur parallélise ses projections sur un
ensemble de fils synchronisés par une barrière atomique ; un jeton paie 168
barrières (7 matrices × 24 couches). C'est ce pool qui limite le débit : 5,3 G
événements/s à 32 fils, effondrement au-delà
(`reports/rapport-inference.md:88-94`, `reports/bilan-multi-materiel.md:54`).
**Où** : `drave-core/src/engine.rs`, `--threads`.

**PushMat** — Encodage de liste « écart + valeur int8 » avec, pour chaque ligne, la
liste de ses destinations : le format qui matérialise le push
(`drave-core/src/list.rs:266`, `reports/rapport-inference.md:31`).

**SparseVec (vecteur creux)** — Structure `{ indices triés, valeurs contiguës }` qui
représente une activation creuse explicite. C'est le type que reçoivent les
accumulateurs `accumulate_push` / `accumulate` (`drave-core/src/engine.rs:29-41`,
`:733-781`). Ses variantes voisines : `SignedDelta` (contributions signées),
`BitmapSign` (masque binaire + signes) et `SparseK` (les k valeurs retenues), dans
`drave-core/src/list.rs` (`reports/rapport-optimisations.md:26`,
`reports/rapport-localite-activation.md:24`).

**SWAR (SIMD Within A Register)** — Technique qui traite plusieurs petites valeurs
en parallèle **à l'intérieur** d'un registre entier (par masques et décalages),
sans instruction SIMD dédiée. Le moteur s'en sert pour décoder huit varints d'un
coup (`reports/rapport-inference.md:32`, `reports/rapport-optimisations.md:19`).
**Réf.** : Henry S. Warren, *Hacker's Delight* — cité sans lien.

**Tête garantie · tête restreinte** — Deux modes d'évaluation : `--tete-restreinte`
limite la tête de sortie à une liste de jetons autorisés, ce qui réduit le trafic
mais fausse la perplexité (mesurée 12,6× trop optimiste) ; `--tete-garantie` est la
version corrigée, qui garantit l'absence de biais
(`reports/rapport-tete-garantie.md:9`, `reports/rapport-tete-restreinte.md:93-96`).

**TraceFlux** — L'écrivain de trace du moteur : il écrit l'en-tête `DRVF`, puis une
liste par (couche, jeton), en version 1, 2 ou 3 selon `DRAVE_TRACE_BLOCS`
(`drave-core/src/model.rs`, `docs/format-flux.md:20-73`).

### Les outils de `tools/` et les bancs du binaire

Ce tableau est un index : chaque outil est un « où » possible pour les entrées de
ce glossaire.

| outil | ce qu'il fait | cité par |
|---|---|---|
| `tools/aiguille.py` | test de l'aiguille (récupération en contexte long) | `reports/rapport-aiguille.md` |
| `tools/analyse_flux.py` | analyse d'une trace, couche par couche | `docs/format-flux.md:11` |
| `tools/profil_flux.py` | densité par couche, part des 10 % les plus forts, export CSV | `docs/roadmap.md:129-149` |
| `tools/analyse_empreinte.py` | empreinte mémoire d'un MoE depuis une trace de routage | `sprints/09:73` |
| `tools/analyse_experts_statique.py` | analyse statique des poids d'experts (jumeaux, sources) | `reports/rapport-empreinte-memoire.md:398` |
| `tools/diff_flux.py` | où deux exécutions divergent, à quel jeton, quels neurones | `docs/roadmap.md:16` |
| `tools/flux_codec.py` | codec Python de référence (lit DRVF v1/v2/v3) | `docs/format-flux.md:180` |
| `tools/trace_compacite.py` | mesure les variantes de compacité d'une trace | `reports/rapport-compacite-trace.md` |
| `tools/verifier_formats.py` | compare un super-bloc déquantifié à `libggml` | `reports/rapport-mla-experts.md:71` |
| `tools/harmony_canonique.py` | identifiant de perplexité au format harmony canonique | `tools/harmony_canonique.py:45` |
| `tools/convertir_clusters.py` | GGUF → `commun.gguf` + `cluster-XX.gguf` + `mapping.tsv` | `docs/format-clusters.md:13` |
| `tools/clusters_moe.py` | découpage MoE : couverture, ventilation, témoins hasard/fréquence | `docs/plan-modeles-lourds.md:70-74` |
| `tools/portes.sh` | portes de non-régression du dépôt | `docs/sprints.md:40` |
| `tools/mhc_v41_synthetique.py` | référence numpy de la chaîne **mHC retardée** de V4.1 + témoins du test Rust | `reports/rapport-v41-mhc.md:97` |
| `tools/verifier_v41_mhc.py` | recalcule hors du moteur la copie 0, les 24 mélanges et la tête de V4.1 depuis les vides et le GGUF | `reports/rapport-v41-mhc.md:85` |
| `tools/hc_synthetique.py` | référence numpy des hyper-connexions de **V4** (opérations ggml de llama.cpp) | `reports/rapport-v4-couches-0-1.md:55` |
| `tools/portes_formats.sh` | confronte les déquantificateurs à `libggml` | `docs/format-clusters.md:148` |
| `tools/verifier_table_types.sh` | compare la table des types ggml à la bibliothèque | `docs/format-clusters.md:148-154` |
| `tools/extraire_tables_ggml.sh` | relève les grilles IQ dans `libggml` et les compare à `formats.rs` | `tools/extraire_tables_ggml.sh:39` |
| `tools/session_report.py` | écrit le rapport de session dans `journal/` | `tools/archive_sessions.py` |
| `tools/ref_logits` (`ref_logits.cpp`) | évalue les mêmes identifiants avec llama.cpp | `reports/rapport-mla-experts.md:146` |
| `tools/compare_logits.py` | compare deux fichiers de logits position par position | `reports/rapport-logits-gpu-vs-cpu.md:28` |
| `tools/compare_etats.py` | compare des vecteurs Drave / llama.cpp | `reports/rapport-v4-couches-0-1.md:26` |
| `tools/proxy_latence.py` | relais qui ajoute un délai par message | `docs/roadmap.md:57` |
| `tools/pair_factice.py` | faux pair réseau qui dit ce qu'il reçoit | `docs/roadmap.md:59` |
| `tools/mla_synthetique.py` | modèle MLA jouet + référence numpy | `docs/plan-mla-vision.md:94` |
| `tools/hc_synthetique.py` | modèle à hyper-connexions jouet (référence numpy + témoins) | `docs/plan-deepseek41-complet.md:171-186` |
| `tools/vision_ref.py` | refait le calcul de vision en numpy | `docs/plan-mla-vision.md:231` |
| `tools/vision_mtmd.py` | sonde `libmtmd` d'ollama par `ctypes` | `docs/plan-mla-vision.md:352` |
| `tools/make_patch.py` | fabrique un greffon `QPAT` pour `--patch` | `reports/rapport-greffon.md:70` |
| `tools/lire_meta_gguf.py` | lit métadonnées et tenseurs GGUF hors moteur | `docs/plan-deepseek41-complet.md:101` |
| `tools/telecharger_modeles.py` | télécharge les modèles lourds par tranches `Range` | `docs/plan-modeles-lourds.md:49` |
| `tools/inventaire_modeles_lourds.sh` | confronte poids annoncés GGUF et tailles HuggingFace | `docs/plan-modeles-lourds.md:122` |
| `tools/mesurer_lecture_experts.py` | rejoue la mesure de lecture d'experts à froid | `reports/rapport-tete-garantie.md:114` |
| `tools/archive_sessions.py` | archive le journal de session (hook git + tâche horaire) | `docs/programme-recherche.md:206` |
| `tools/preparer_colab.sh` / `tools/colab_cote_local.sh` | préparent la démonstration Colab | `docs/colab-reparti.md:17` |
| `tools/sprint.sh` | chronomètre et rédige la trame de sprint | `docs/sprints.md:8-17` |
| bancs du binaire | `--banc-kv`, `--banc-mla`, `--banc-topk`, `--banc-vision`, `--gpu-banc` | `docs/plan-gpu-topk.md:36`, `docs/plan-mla-vision.md:229` |

### Drapeaux de ligne de commande et variables d'environnement

Le moteur expose **93 drapeaux `--xxx`** reconnus et **39 variables `DRAVE_*`**
déclarées (`drave-core/src/main.rs:17-27`, `:580-742`). L'audit du 30/09 en
comptait 84 et 26, et montrait que **46 drapeaux (55 %) étaient ignorés**, dont 20
classés rouges (`reports/rapport-drapeaux-ignores.md:31-32`, `:240-245`). Depuis,
`--options-actives` affiche le tableau de bord des réglages réellement appliqués et
`--options-strict` transforme un drapeau inconnu en erreur : au 30/09 ce dernier
n'existait pas encore, il est aujourd'hui implémenté (`main.rs:619`).

| famille | drapeaux / variables |
|---|---|
| chemin d'exécution | `--push`, `--dense`, `--auto`, `--keep`, `--q4`, `--q4-attn`, `--q4-ffn`, `--q4-tout`, `--bits`, `--abits` |
| attention et parcimonie | `--attn-topk`, `--qk-topk`, `--moe-topk`, `--act-thresh`, `--act-topk`, `--act-renorm`, `--attn-window`, `--sans-fenetre`, `--swa-pattern`, `--attn-sinks`, `--sans-yarn`, `--topk-q/-k/-v/-o/-gate/-up/-down` |
| trace et rejeu | `--trace-flux`, `--trace-couches`, `--flux-forcer`, `--logits-bin`, `--profil-neurones`, `--neurones-sortie` |
| transport | `--flux-serveur`, `--ppl-reparti`, `--couches-locales`, `--flux-liste`, `--flux-blocs`, `--lot` |
| matériel | `--threads`, `--pin`, `--plan`, `--materiel`, `--gpu-banc`, `--banc-kv`, `--banc-mla`, `--banc-topk`, `--banc-vision` |
| modèles | `--config`, `--tensors`, `--plan`, `--couches`, `--tete-partielle`, `--patch`, `--tete-restreinte`, `--tete-garantie`, `--sonder-engram` |
| GPU | `DRAVE_GPU`, `DRAVE_GPU_TETE`, `DRAVE_GPU_KV`, `DRAVE_GPU_TOPK`, `DRAVE_GPU_EXPERTS`, `DRAVE_GPU_EXPERTS_GO` |
| cache KV | `DRAVE_KV_BITS`, `DRAVE_KV_F16`, `DRAVE_KV_K_F16`, `DRAVE_KV_K_F32`, `DRAVE_KV_V_F32` |
| trace et diagnostic | `DRAVE_TRACE_BLOCS`, `DRAVE_TRACE_EXPERTS`, `DRAVE_TRACE_HC`, `DRAVE_FLUX_VERIF`, `DRAVE_DEBUG_FLUX`, `DRAVE_DEBUG_MLA`, `DRAVE_DEBUG_ETAT` |
| divers | `DRAVE_MMAP`, `DRAVE_PRELIRE`, `DRAVE_PRELIRE_TOUT`, `DRAVE_CLUSTERS`, `DRAVE_YARN`, `DRAVE_YARN_NON`, `DRAVE_YARN_MSCALE`, `DRAVE_VISION_TEXTE`, `DRAVE_HARMONY_TRACE`, `DRAVE_Q8_BLOCS`, `DRAVE_SANS_EMPRUNT` |

Les anciennes variables `QT_*` ne font plus rien : elles déclenchent un
avertissement au lieu d'être des alias silencieux (`docs/histoire.md:46-60`).

---

