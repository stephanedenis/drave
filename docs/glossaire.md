# Glossaire raisonné de Drave

Ce document explique **tout le vocabulaire** employé dans `docs/` (18 documents) et
`reports/` (60 rapports, plus 9 fichiers dans `sprints/`), pour quelqu'un qui ne
connaît ni les grands modèles de langage, ni le matériel, ni le vocabulaire de la
mesure de performance. Il se lit seul : chaque notion est définie sur place, et
chaque définition renvoie au fichier du dépôt qui l'emploie.

---

## Mode d'emploi

**Ce que contient une entrée.** Chaque entrée suit le même patron :

> **Terme** *(forme développée française ; forme anglaise)* — définition en une à
> trois phrases, sans prérequis. La définition dit **où** le moteur s'en sert
> (fichier, outil ou drapeau du dépôt, avec un numéro de ligne quand il aide) et,
> quand une source externe stable existe, la référence **Réf.** (article,
> spécification, documentation officielle).

**Conventions de lecture.**

- `chemin:ligne` renvoie à un fichier **du dépôt**, à la ligne indiquée. Exemple :
  `docs/vision.md:34`.
- Les liens externes pointent vers des articles ou des spécifications ; quand je
  n'ai pas pu vérifier l'adresse, je cite l'article **par son titre et ses
  auteurs, sans lien** — c'est une règle du dépôt, on n'invente pas d'URL.
- Un terme qui a **plusieurs sens** dans le corpus est signalé ; c'est le cas de
  *CDC*, *mode*, *porte*, *grappe* et *tête*.
- Les valeurs numériques citées ici sont celles des documents, **à leur date**.
  Elles ne sont pas re-mesurées par ce glossaire ; la section
  « Points relevés, non corrigés » en bas signale celles qui se contredisent.

**Ce que ce document n'est pas.** Ce n'est ni un tutoriel d'inférence, ni un
résumé de la feuille de route. Il ne corrige aucun autre fichier : les erreurs,
contradictions et chiffres périmés croisés en le rédigeant sont **listés à la fin**,
avec `fichier:ligne` et citation, sans être modifiés.

**Périmètre.** `docs/` (18 documents) et `reports/` (60 rapports) ; les 9 fichiers
de `sprints/` sont couverts pour leur vocabulaire propre (boxing, cérémonie,
porte). Le code est cité pour dire *où* un terme est utilisé (`drave-core/src/`,
`tools/`), mais le glossaire ne décrit pas le code ligne à ligne. Les fichiers
`README.md`, `REPRISE.md` et `Qtrinet-bootstrap.md` sont à la racine, hors
périmètre : ils sont signalés quand ils portent un chiffre utilisé partout.

---

## Parcours de lecture conseillé

**Si tu ne lis qu'un document, lis `docs/vision.md`** (279 lignes) : c'est la
vision — des listes d'activation plutôt que des matrices, cinq axes, ce que le
projet n'est pas, et le nom. Tout le reste du dépôt en découle.

Ensuite, dans cet ordre :

1. **`docs/histoire.md`** (78 lignes) — pourquoi le projet s'appelait Qtrinet et
   s'appelle Drave, et la table de conversion des anciens noms de variables. À
   lire tôt : tous les rapports antérieurs au 30/09/2026 emploient encore
   « Qtrinet », `QT_*` et `qtrinet-core`.
2. **`docs/roadmap.md`** (311 lignes) — l'état réel de chaque chantier, phase par
   phase, avec les chiffres et leur date. C'est le document qui dit ce qui est
   fait (✅), en cours (🔬), à faire (⏳) ou bloqué (🧱).
3. **`docs/format-flux.md`** (188 lignes) — le format `DRVF` : ce qu'est une trace,
   comment elle se relit, et le protocole réseau **v5** avec ses cinq modes. Le
   cœur technique du projet est là.
4. **`docs/sprints.md`** (75 lignes) — comment le travail est découpé (sprints de
   2 h), ce qu'est une « porte », une rétrospective, un engagement de fin de
   sprint. Indispensable pour comprendre le ton des rapports.
5. **`reports/rapport-inference.md`** — la mesure fondatrice : un moteur de
   2 319 lignes de Rust sans dépendance, 5,3 G événements/s sur CPU, 16 jetons
   identiques sur 16 à la référence numpy.
6. **`reports/rapport-croisement-push-pull.md`** — la mesure qui fixe la frontière
   du projet : le chemin « push » (listes) bat le dense en dessous de ~22 % de
   densité d'activation, et perd au-dessus. Tout le reste en dépend.
7. **`docs/contexte-long.md`** — ce que « 1 M de jetons de contexte » veut dire, et
   par où ça casse (préremplissage, bande passante du cache, rotation).
8. **`docs/format-clusters.md`** — comment un modèle est éclaté en grappes
   (`commun.gguf` + `cluster-XX.gguf`) et pourquoi c'est le mécanisme de placement.
9. **`docs/plan-deepseek41-complet.md`** — le chantier en cours : exécuter un
   modèle réel (V4.1) **en listes**, avec ses deux portes (correction et Drave).

Pour aller plus loin : `docs/programme-recherche.md` (la thèse et ses critères
d'arrêt), `docs/comparaison-spiking.md` (ce que les réseaux à spikes changent),
`docs/plan-mla-vision.md` (attention latente et vision), et — quand un chiffre
semble contradictoire — `reports/rapport-coherence-docs-2.md`, l'audit qui recense
les affirmations périmées du corpus.

À la racine, `README.md` (36 ko) donne l'état général et `REPRISE.md` (81 ko) le
journal de reprise détaillé ; ils emploient le même vocabulaire que ce glossaire.

---

## 1. Le projet, ses noms, sa méthode

**A/B (écart A/B)** — Comparaison de deux exécutions ne différant que par un
réglage, sur le même texte et les mêmes jetons. Le dépôt en fait la règle quand un
chiffre absolu n'est pas reproductible : « seul l'écart A/B fait foi »
(`docs/plan-gpu-topk.md:99`). **Où** : `--attn-topk` contre sans top-k,
`docs/contexte-long.md:557-567`.

**Banc (bench)** — Dispositif de mesure isolé qui fait tourner une seule partie du
moteur sur des données choisies, pour que la bonne réponse soit connue d'avance.
Le dépôt en a plusieurs : `--banc-kv`, `--banc-mla`, `--banc-topk`, `--banc-vision`,
`--gpu-banc` (`drave-core/src/main.rs`). Un banc qui passe ne prouve pas qu'il
mesure ce qu'on croit : `docs/sprints.md:69-73`.

**Boxing** — Règle des sprints : 2 h chronométrées, on s'arrête quand la boîte est
pleine même si c'est presque fini, et ce qui reste va au planning suivant.
`docs/sprints.md:6-17`. **Où** : `tools/sprint.sh`.

**CDC** *(polysémie)* — Dans le corpus, **deux sens** :
1. **cahier des charges** : le document d'origine du projet, `Qtrinet-bootstrap.md`,
   qui imposait l'inférence ternaire sur FPGA, « 100 % logique, sans DSP »
   (`docs/histoire.md:11`) ;
2. **Clock Domain Crossing** : traversée de domaines d'horloge sur le FPGA,
   contrainte tenue sans perte de fréquence (`reports/bilan-multi-materiel.md:68`).
Lire le contexte avant de traduire. **Réf.** : pour le second sens, voir la
documentation Intel « Stratix V Device Handbook », section Clocking.

**Créneau long** — Unité de travail de 3 h, entre le sprint (2 h) et la journée
(8 h) ; produit deux à trois chantiers (`docs/sprints.md:58-63`).

**Definition of done (engagement de fin de sprint)** — Liste non négociable pour
fermer un sprint « vert » : `cargo test --release` passe, les portes de
non-régression sont intactes, tout est commité, la machine est rendue, tout chiffre
annoncé a sa source (`docs/sprints.md:33-46`).

**Drave** — Nom du projet depuis le 30/09/2026 : *stream of logs*, « le flux des
listes », et en français la drave, ces billots confiés à la rivière. Le mot porte
trois propriétés : ça coule, ça se répartit, ça se surveille
(`docs/vision.md:260-273`, `docs/histoire.md:18-24`). **Où** : crate `drave-core`,
binaire `drave`, variables `DRAVE_*`, noyaux `drave_gpu.*`.

**Écart (0,00e0)** — Différence entre le résultat d'une exécution locale et celui
d'une exécution découpée ou transportée. `0,00e0` signifie « aucun écart
représentable » : c'est le critère de fidélité du transport dense
(`docs/roadmap.md:55`, `docs/format-flux.md:185`).

**Fait · mesuré · projeté · déduit** — Étiquettes de confiance du dépôt. *Mesuré* :
chiffre obtenu sur cette machine, commande citée ; *projeté* : extrapolé d'un
modèle ou d'une limite matérielle ; *déduit* : conséquence d'une autre mesure. Le
bilan multi-matériel les distingue colonne par colonne (`reports/bilan-multi-materiel.md:33-40`).

**Harnais (harness)** — Petit montage de test autonome, souvent en Python, qui
enveloppe un composant pour le mesurer ou le comparer à une référence. Exemples :
harnais de perplexité (`src/bpe_np.py`, `src/transformer_np.py`), harnais MLA
(`tools/mla_synthetique.py`, `--banc-mla`), harnais de vision (`tools/vision_ref.py`).
Voir `reports/rapport-harnais.md`.

**Journal de session** — Historique horodaté de tout ce qui a été mesuré, archivé
automatiquement à chaque commit (`tools/archive_sessions.py`, hook git + tâche
horaire). Le journal est la mémoire brute : il n'est **pas** réécrit lors des
renommages (`docs/histoire.md:38-43`, `docs/programme-recherche.md:206-208`).
**Où** : `journal/`.

**Mesure entrelacée · machine au calme** — Protocole : mesurer les configurations
comparées en alternance, parce que la charge de fond (bureau, autres projets) fait
varier le temps mural de 30 % ; et préférer les mesures déterministes (perplexité,
comptes d'événements) aux mesures de temps (`docs/programme-recherche.md:201-205`,
`reports/rapport-campagne-parcimonie.md:8-10`).

**Non-régression (porte de non-régression)** — Valeur de référence qu'une
modification ne doit pas dégrader. Les portes du dépôt sont : Qwen2.5-0.5B à
contexte 256 = **19,3885** ; gpt-oss à contexte 256 = **15,6017** ; Qwen3-30B en
clusters = **799,8557** ; le banc réparti dense = **0,00e0**
(`docs/sprints.md:38-41`, `docs/plan-gpu-topk.md:101`). **Où** : `tools/portes.sh`,
`cargo test --release`.

**Porte de correction** — Comparaison à une référence **externe** (llama.cpp ou une
implémentation numpy indépendante) qui sert à corriger le moteur, jamais de but.
« La conformité à llama.cpp est une porte de correction, pas le but : le but est de
conduire des flux » (`docs/plan-modeles-lourds.md:83-85`,
`docs/plan-deepseek41-complet.md:9`). **Depuis le 03/10 (bloc 23) elle a des critères
mesurés**, et un outil qui rend le verdict au lieu d'une impression
(`tools/compare_logits.py --porte`, branché dans `tools/portes.sh`) : corrélation des
logits **par position** ≥ 0,95 au minimum et ≥ 0,98 en moyenne, top-1 identique
≥ 85 %, perplexité à moins de 10 % — ce dernier critère **seulement au-delà de 64
prédictions**, parce que sur une fenêtre de 4 jetons le même moteur diverge de 25 %
et sur 63 prédictions de 6,4 % (mesuré sur V4-Flash,
`docs/plan-deepseek41-complet.md:385-430`). **La perplexité seule n'est pas
l'instrument** : sur une fenêtre courte elle amplifie le chaos au lieu de mesurer la
fidélité.

**Porte (de décision)** — Un chiffre, mesuré sur cette machine, qui décide de
continuer ou d'abandonner une branche ; « une porte non franchie arrête la
branche — pas de poursuite par inertie » (`docs/programme-recherche.md:134-135`,
`:210`). Exemples : *Porte A* (une variante bat le modèle de base de ≥1 % de
perplexité), *Porte C* (apprendre un fait à l'inférence sans oubli catastrophique).

**Porte Drave** — Épreuve propre au projet, opposée à la porte de correction :
nombre d'événements par jeton non nul, trace écrite puis **rejouée à l'identique**,
découpage en grappes qui donne la même perplexité, flux nouveau lisible par un
outil d'analyse (`docs/plan-deepseek41-complet.md:134-141`). Depuis le 03/10
(bloc 22), « rejouée à l'identique » est **défini et vérifié** : aucune liste
manquante **et** écart de perplexité ≤ 1e-5 (mesuré : 4,5e-06 sur V4-Flash, 1,6e-06
sur Qwen ; `docs/plan-deepseek41-complet.md:347-351`). L'écart ne peut pas être nul :
la trace porte des activations déjà quantifiées, que le rejeu requantifie.

**Qtrinet** — Premier nom du projet, du nom d'un réseau ternaire sur un cluster de
cartes **Stratix V** ; le cahier des charges d'origine, `Qtrinet-bootstrap.md`, est
conservé tel quel comme pièce datée. Les variables `QT_*` ne font plus rien : le
moteur prévient au lieu de laisser croire qu'une option est active
(`docs/histoire.md:11`, `:46-60`).

**Rapport** — Document de `reports/` consignant une campagne : commande exacte,
chiffres, erreurs trouvées, réserves. Un rapport porte ses propres corrections,
souvent en tête (bandeau « État ») ou en sections « CORRIGÉ »
(`reports/rapport-compacite-trace.md:13-18`).

**Rejeu** — Réinjection d'une trace enregistrée dans le moteur
(`--flux-forcer <trace>`) : les activations calculées sont remplacées par celles du
fichier, et si le résultat est identique, « une liste suffit à continuer le
calcul » (`docs/roadmap.md:196-213`, `docs/format-flux.md:6-8`).

**Relire · relecture adverse · relecture déléguée** — Trois niveaux de relecture.
La relecture *adverse* cherche activement à casser une affirmation ; la relecture
*déléguée* est confiée à un autre agent et compte comme une tâche du sprint.
« Trois relectures adversariales ont trouvé 28 défauts sur un créneau, presque tous
par lecture » (`docs/sprints.md:69-73`, `reports/rapport-coherence-vision.md:3-6`).

**Rétrospective** — Partie de la cérémonie de fin de sprint : *garder* / *changer* /
*doute*. « Une rétro qui ne change rien n'est pas une rétro : chaque "changer" doit
devenir une action du sprint suivant » (`docs/sprints.md:27-29`).

**Session · sprint** — Une session (journée) peut contenir plusieurs sprints
(2 h chacun) ; un index de session est écrit dans
`reports/rapport-session-*.md` (`docs/sprints.md:56-65`).

**Trace (de flux)** — Enregistrement, couche par couche et jeton par jeton, des
neurones actifs (indice + valeur) et de leur échelle. La trace est à la fois le
journal d'exécution, la matière du rejeu, le contrat d'échange réseau et la donnée
d'analyse (`docs/format-flux.md:1-18`). **Où** : `--trace-flux`.

**Verdict négatif** — Résultat qui ferme une piste, consigné comme les autres.
Exemples : le cache d'experts MXFP4 en VRAM (+6 %, « à ne pas activer par défaut »,
`docs/contexte-long.md:355-366`), l'épinglage NUMA (« mesuré, perdant »,
`docs/convertisseur.md:236-242`), le lot dense sur la tête de sortie (« ne gagne
rien », `reports/rapport-prefill-par-lots.md:131-136`).

---

## 2. Modèles et architectures

**Attention creuse** — Attention restreinte aux k meilleures clés par requête
(`--attn-topk`) ou à une fenêtre (`--attn-window`). Mesure contre-intuitive du
dépôt : restreindre aux 256 meilleures clés **améliore** la perplexité de 21 % sur
du texte brut, parce que l'attention lointaine ajoute du bruit
(`docs/contexte-long.md:557-578`).

**Attention (self-attention)** — Mécanisme par lequel chaque jeton d'une séquence
compare sa « requête » (Q) aux « clés » (K) de tous les jetons précédents, puis
mélange leurs « valeurs » (V) selon ces scores. C'est le poste dont le coût croît
avec la longueur du contexte (`reports/rapport-attention-creuse.md:5-6`).
**Où** : `drave-core/src/model.rs`, `--attn-window`, `--attn-topk`.
**Réf.** : Vaswani et al., *Attention Is All You Need*, [arXiv:1706.03762](https://arxiv.org/abs/1706.03762).

**BatchNorm (normalisation par lot)** — Normalisation qui centre et réduit les
activations sur un lot d'exemples. Les réseaux à spikes de référence l'utilisent
au lieu de LayerNorm, qui « ne s'applique pas » à eux (`docs/comparaison-spiking.md:113-116`).
**Réf.** : Ioffe & Szegedy, *Batch Normalization*, [arXiv:1502.03167](https://arxiv.org/abs/1502.03167).

**Biais (bias)** — Terme additif ajouté après une projection. Les oublier est
« l'erreur classique de ce dépôt » : elle a coûté 39,80 → 20,84 de perplexité sur
gpt-oss et fait diverger tout le ViT (`docs/plan-mla-vision.md:171-173`,
`docs/convertisseur.md:319-323`).

**BPE (Byte Pair Encoding ; codage par paires d'octets)** — Algorithme de
tokenisation qui découpe le texte en morceaux fréquents, appris statistiquement.
Le moteur en a une implémentation Rust conforme au pré-tokenizer Qwen2 (737 cas sur
737) ; le `src/bpe_np.py` du harnais, lui, s'en écarte sur 5 points (5,2 % des
identifiants) (`reports/rapport-inference.md:157-168`). **Où** : `src/tokenizer.rs`.
**Réf.** : Sennrich et al., *Neural Machine Translation of Rare Words with Subword
Units*, [arXiv:1508.07909](https://arxiv.org/abs/1508.07909).

**CSA (Compressed Sparse Attention ; attention compressée creuse)** — Régime
d'attention de DeepSeek-V4 où les clés sont regroupées en blocs compressés, et où
un **indexeur** ne sélectionne qu'un sous-ensemble de blocs candidats par jeton.
V4.1 a 18 couches CSA (ratio 2), V4-Flash en a 21 (ratio 4)
(`docs/plan-deepseek41-complet.md:100-130`, `reports/rapport-v4-hca.md:96`).
**Réf.** : à citer par son titre, *DeepSeek-V4 Technical Report* — je n'ai pas
d'URL vérifiable pour ce document.

**DSA** — Sigle employé comme nom d'architecture GGUF (`glm-dsa`, pour GLM-5.3),
variante « à indexeur » de l'attention creuse : le modèle choisit les blocs de clés
à noter au lieu de toutes les noter (`docs/plan-modeles-lourds.md:93`,
`reports/rapport-mla-experts.md:124`). À ne pas confondre avec la couche CSA
proprement dite.

**Engram** — Table d'adresses creuse, adressée par hachage de n-grammes (motifs de
1 à 4 jetons) : le modèle y lit des rangées de mémoire externe plutôt que de
recalculer. Dans V4.1, deux couches d'engram pèsent 203 Go sur 365,7 Go, mais une
session de 10 000 jetons n'en touche que ~4,6 Mo — d'où l'intérêt du `mmap`
(`docs/plan-deepseek41-complet.md:53`, `reports/rapport-empreinte-memoire.md:7-10`).

**Expert (MoE)** — Sous-réseau spécialisé qu'un routeur allume pour certains
jetons seulement. « Un expert qui ne tire pas coûte zéro octet » : c'est l'avantage
structurel revendiqué par le projet (`docs/programme-recherche.md:33-35`).

**Expert partagé (`shexp`)** — Expert **toujours actif**, en plus des experts
routés : ses tenseurs (`ffn_*_shexp.weight`) existent dans le GGUF mais le moteur ne
les calcule pas encore — un manque nommé par `--config`
(`reports/rapport-mla-experts.md:128-131`).

**Fenêtre glissante (sliding window attention, SWA)** — Attention limitée aux N
derniers jetons, apprise par le modèle. « La fenêtre déclarée par le modèle n'est
pas un réglage, c'est une propriété » : l'élargir détruit la perplexité (×11)
(`docs/contexte-long.md:575-578`). **Où** : `attention.sliding_window = 128`,
`--swa-pattern`, `--attn-window`.
**Réf.** : Jiang et al., *Mistral 7B*, [arXiv:2310.06825](https://arxiv.org/abs/2310.06825).

**FFN (Feed-Forward Network ; réseau à propagation avant)** — Le bloc qui suit
l'attention dans chaque couche : deux ou trois projections avec une non-linéarité.
Dans un MoE, il est remplacé par des experts routés. **Où** : tenseurs `ffn_gate`,
`ffn_up`, `ffn_down` (`docs/format-clusters.md:20-23`).

**GELU (Gaussian Error Linear Unit)** — Non-linéarité lisse proche de ReLU. Le
projecteur de vision en utilise un (approximation d'erf d'Abramowitz-Stegun
7.1.26), mais **pas** la tour du ViT, qui utilise SiLU
(`docs/plan-mla-vision.md:187-201`). **Réf.** : Hendrycks & Gimpel,
*Gaussian Error Linear Units*, [arXiv:1606.08415](https://arxiv.org/abs/1606.08415).

**GQA (Grouped-Query Attention ; attention à requêtes groupées)** — Compromis entre
l'attention multi-têtes et MQA : plusieurs têtes de requête partagent une même
tête de clé/valeur, ce qui réduit le cache. Qwen2.5-0.5B a 14 têtes de requête pour
2 têtes KV (`reports/rapport-modele-reel.md:3`). **Réf.** : Ainslie et al.,
*GQA: Training Generalized Multi-Query Transformer Models*,
[arXiv:2305.13245](https://arxiv.org/abs/2305.13245).

**HCA (attention compressée à ratio élevé)** — Régime d'attention de DeepSeek-V4
où un bloc de clés est résumé en un petit nombre de valeurs, avec une porte softmax
par canal ; 20 couches de V4-Flash, validées à 0,999992 de corrélation avec
llama.cpp au 128ᵉ jeton (`docs/plan-deepseek41-complet.md:226-237`,
`reports/rapport-v4-hca.md:5`).

**Hyper-connexions (HC)** — Mécanisme de V4.1 : l'état résiduel est dupliqué en 4
copies, puis remélangé à chaque couche par des poids (`pre`, `post`, `comb`)
normalisés par **Sinkhorn** sur 20 itérations. Sans ce mélange, tout ce qui suit a
la mauvaise entrée — et l'erreur est silencieuse
(`docs/plan-deepseek41-complet.md:171-186`, `reports/rapport-v4-couches-0-1.md:55`).
**Où** : `hc_retarde`, `--tete-partielle`.

**mHC retardé (chaîne retardée de V4.1)** — Dans **V4** (`deepseek4`), chaque
raccord (attention, FFN) replie l'entrée avec **ses propres** coefficients ; dans
**V4.1** (`deepseek41`), les coefficients servent au raccord **suivant** :
l'attention se replie avec la `pre` de la FFN précédente, la FFN avec la `pre` de
l'attention courante, et la **tête** — qui n'a aucun poids appris chez V4.1 — avec
la `pre` de la dernière FFN. Au tout premier raccord, la copie 0 est prise telle
quelle. Confondre les deux chaînes change la sortie de 67 % sur un témoin
synthétique : ce n'est pas une variante d'écriture
(`reports/rapport-v41-mhc.md:31-48`, `tools/mhc_v41_synthetique.py`).
**Où** : `general.architecture`, `--tete-partielle`.
**Réf.** : vLLM, `vllm/models/deepseek_v41/nvidia/model.py` (`hc_collapse_triton`,
`mhc_shifted_post_pre`), <https://github.com/vllm-project/vllm>.

**Cache compressé partagé (`kv_source_layer_ids`)** — Dans V4.1, seules quelques
couches (**2, 8, 14, 20**) portent un compresseur et publient les clés compressées ;
les couches suivantes (3..7, 9..13, 15..19, 21..39) **lisent les mêmes clés** au
lieu de calculer les leurs. Un compresseur calculé couche par couche donnerait
d'autres clés — un résultat faux qui ne casse rien. Le moteur indexe donc les
tampons par **source** (`comp_source`), et la preuve que la couche 3 lit bien
l'état de la 2 est un contrôle positif/négatif : sa sortie change de 1,30 à 2,16
selon que sa source a tourné ou non, tandis que la sortie de la source est
identique au bit (`reports/rapport-v41-mhc.md`, §6).
**Où** : `comp_source`, `Mla4::a_compresseur`.

**Compression de contexte (ratio 1, 2, 4, 128)** — Résumer `ratio` jetons en un
seul latent de clé, afin que l'attention ne croisse plus avec la longueur. V4-Flash
mélange **CSA** (ratio 4, fenêtre à chevauchement) et **HCA** (ratio 128) ; V4.1
utilise **2** (softmax par canal sur le groupe, apprise porte) et **1** (un latent
par jeton, sans porte ni `ape`). Le RoPE du bloc est appliqué à la position du
**premier** jeton du groupe, avec la base `compress_rope_theta` (160 000)
(`reports/rapport-v4-hca.md:40-70`, `reports/rapport-v41-mhc.md:120-128`).
**Où** : `compress_ratios`, `rope_base_compresse`.
**Réf.** : vLLM, `vllm/models/deepseek_v41/compressor.py` (`DeepseekCompressor`).

**Indexeur (lightning indexer)** — Petit réseau qui note des blocs de clés et n'en
retient qu'un sous-ensemble (2 048 blocs candidats) avant l'attention proprement
dite. C'est « le flux le plus intéressant du modèle : il décide de ce que
l'attention voit » (`docs/plan-deepseek41-complet.md:267-285`,
`reports/rapport-v4-hca.md:96`).

**Jeton (token)** — Unité de texte traitée par le modèle : un mot court, un
fragment de mot ou un signe. Le moteur raisonne en jetons, jamais en caractères
(`docs/format-flux.md:29`). **Où** : `--tokenize`, `src/tokenizer.rs`.

**k-WTA (k-Winners Take All ; les k gagnants emportent tout)** — Parcimonie
imposée : ne garder que les k plus grandes activations d'un vecteur, les autres
passant à zéro. Mesurée « dix fois meilleure » qu'un seuil absolu à sparsité égale
(`reports/rapport-parcimonie-imposee.md:24`, `:42-54`). **Où** : `--act-topk`.

**KV (cache clé-valeur)** — Mémoire des clés et valeurs déjà calculées pour les
jetons précédents, relue à chaque nouveau jeton. À contexte long, c'est le second
mur du projet : 77 Go en f32 à 1 M de jetons pour gpt-oss, 9,7 Go en int4
(`docs/contexte-long.md:29-37`, `:61-73`). **Où** : `KvCache`, `DRAVE_KV_BITS`,
`DRAVE_GPU_KV`. **Réf.** : Pope et al., *Efficiently Scaling Transformer
Inference*, [arXiv:2211.05102](https://arxiv.org/abs/2211.05102).

**LayerNorm (normalisation de couche)** — Normalisation sur les canaux d'un même
jeton, qui stabilise l'entraînement. Voir aussi RMSNorm.
**Réf.** : Ba, Kiros & Hinton, *Layer Normalization*,
[arXiv:1607.06450](https://arxiv.org/abs/1607.06450).

**LIF (Leaky Integrate-and-Fire ; neurone à intégration et décharge)** — Neurone
des réseaux à spikes : il accumule son entrée et « décharge » un spike 0/1 quand un
seuil est franchi. Il décharge à R̂ ≈ 0,15 chez SpikeGPT, d'où 6,7× moins
d'événements (`docs/comparaison-spiking.md:36-40`). **Réf.** : Gerstner & Kistler,
*Spiking Neuron Models* (Cambridge University Press, 2002) — cité sans lien.

**Logits** — Vecteur des scores bruts donnés par le modèle à chaque jeton possible
du vocabulaire, avant normalisation en probabilités. Le moteur en écrit pour
comparer deux exécutions (`--logits-bin`, `tools/compare_logits.py`).

**LoRA (Low-Rank Adaptation ; adaptation à rang faible)** — Remplacer une grosse
matrice par le produit de deux petites matrices (une « descente » puis une
« remontée »), ce qui réduit le nombre de paramètres. C'est le principe des
projections de MLA et de la sortie groupée de V4 (`q_lora_rank`, `kv_lora_rank`,
`o_lora_rank` ; `docs/plan-mla-vision.md:26-53`,
`docs/plan-deepseek41-complet.md:78-88`). **Réf.** : Hu et al., *LoRA: Low-Rank
Adaptation of Large Language Models*, [arXiv:2106.09685](https://arxiv.org/abs/2106.09685).

**MLA (Multi-head Latent Attention ; attention latente multi-têtes)** — Variante
d'attention qui ne stocke qu'un **latent** par jeton (une petite dizaine de
valeurs) et reconstruit clés et valeurs à la lecture ; le cache KV devient ~50×
plus petit. Validée contre numpy à 5,2e-7 et contre llama.cpp à 0,999024 sur
GLM-5.3 (`docs/plan-mla-vision.md:8-90`, `reports/rapport-mla-experts.md`).
**Réf.** : DeepSeek-AI, *DeepSeek-V2*, [arXiv:2405.04434](https://arxiv.org/abs/2405.04434).

**MoE (Mixture of Experts ; mélange d'experts)** — Architecture où chaque jeton
n'est traité que par quelques experts choisis par un routeur (par exemple 8 sur
128). « Un modèle à cent experts dont deux tirent coûte le prix de deux »
(`docs/programme-recherche.md:33-35`). **Réf.** : Fedus, Zoph & Shazeer,
*Switch Transformers*, [arXiv:2101.03961](https://arxiv.org/abs/2101.03961).

**MQA (Multi-Query Attention ; attention à requête unique)** — Toutes les têtes de
requête partagent une seule tête de clé/valeur. MLA et V4 en sont des variantes ou
des descendants (`docs/plan-mla-vision.md:33`).
**Réf.** : Shazeer, *Fast Transformer Decoding: One Write-Head is All You Need*,
[arXiv:1911.02150](https://arxiv.org/abs/1911.02150).

**mRoPE (rotation 2-D, rotary position embedding multimodale)** — Rotation
positionnelle appliquée en quatre blocs (ligne, colonne, ligne, colonne) pour des
entrées 2-D comme les patchs d'image, au lieu de la rotation scalaire des jetons de
texte. La convention exacte a été lue dans `clip.cpp` de llama.cpp
(`docs/plan-mla-vision.md:500-535`, `:682-711`). **Réf.** : Qwen Team,
*Qwen2.5-VL Technical Report*, [arXiv:2502.13923](https://arxiv.org/abs/2502.13923).

**MTP (Multi-Token Prediction ; prédiction multi-jetons) et décodage spéculatif** —
Prédire plusieurs jetons d'avance, ou faire proposer des jetons par un petit modèle
puis les vérifier en bloc, pour accélérer la génération. Dans le corpus, MTP
n'apparaît que sous le nom `dspark_*` de V4.1, décrit comme « décodage spéculatif,
cibles 37-39 » (`docs/plan-deepseek41-complet.md:86`). **Réf.** : DeepSeek-AI, *DeepSeek-V3
Technical Report* (MTP), [arXiv:2412.19437](https://arxiv.org/abs/2412.19437) ;
Leviathan et al., *Fast Inference from Transformers via Speculative Decoding*,
[arXiv:2211.17192](https://arxiv.org/abs/2211.17192).

**NLL (Negative Log-Likelihood ; log-vraisemblance négative)** — Perte d'une
prédiction : `−log(p)` du jeton réel, en nats. Plus elle est basse, meilleur est le
modèle ; la perplexité est son exponentielle. **Où** : `tools/compare_logits.py`,
`reports/rapport-gpt-oss-perplexite.md:76`. **Réf.** : Goodfellow, Bengio &
Courville, *Deep Learning*, chapitre 5 (maximum de vraisemblance) —
[deeplearningbook.org](https://www.deeplearningbook.org/contents/ml.html).

**Patch · ViT · projecteur (mmproj)** — Un *patch* est un carré d'image (14 × 14
pixels) traité comme un jeton ; le *ViT* est la tour de vision qui les encode ; le
*projecteur* (`mmproj`) traduit ces vecteurs vers la dimension du modèle de texte.
Chaîne démontrée de l'image aux logits sur Qwen2.5-VL-7B
(`docs/plan-mla-vision.md:654-671`). **Réf.** : Dosovitskiy et al., *An Image is
Worth 16x16 Words*, [arXiv:2010.11929](https://arxiv.org/abs/2010.11929) ;
Radford et al., *CLIP*, [arXiv:2103.00020](https://arxiv.org/abs/2103.00020).

**« Perdu au milieu » (lost in the middle)** — Comportement observé des modèles
longs : ils retrouvent une information placée au début ou à la fin d'un contexte,
mais beaucoup moins bien au milieu. Le test de l'aiguille du dépôt retrouve
exactement ce motif (`reports/rapport-aiguille-topk.md:52-58`).
**Réf.** : Liu et al., *Lost in the Middle*, [arXiv:2307.03172](https://arxiv.org/abs/2307.03172).

**Perplexité (PPL)** — Exponentielle de la perte moyenne par jeton : mesure
d'« étonnement » du modèle sur un texte. Plus elle est basse, mieux le modèle
prédit ; un écart de quelques centièmes de pour cent est significatif sur un même
corpus, mais **deux perplexités sur deux corpus ne se comparent pas**
(`docs/format-flux.md:181-183`, `docs/contexte-long.md:316-319`).
**Réf.** : Brown et al., *An Estimate of an Upper Bound for the Entropy of
English* — [aclanthology.org/J92-1002](https://aclanthology.org/J92-1002/).

**Préremplissage (prefill) · décodage (decode)** — Le préremplissage traite tout le
prompt d'un coup (parallélisable) ; le décodage produit les jetons un par un
(séquentiel). « Le décodage restera séquentiel ; c'est le préremplissage qui est
parallèle par nature » (`docs/vision.md:160-162`) ; le mode 3 du protocole sert au
préremplissage (`docs/format-flux.md:127-134`).

**Puits d'attention (attention sinks)** — Clé virtuelle de valeur nulle, apprise,
qui ne compte que dans le dénominateur du softmax : elle sert de « poubelle » où le
modèle jette son attention. Les oublier fausse toute la distribution, pas seulement
la queue (`docs/convertisseur.md:286-288`, `docs/plan-gpu-topk.md:107-109`).
**Réf.** : Xiao et al., *Efficient Streaming Language Models with Attention Sinks*,
[arXiv:2309.17453](https://arxiv.org/abs/2309.17453).

**R̂ (taux de décharge)** — Proportion d'activations non nulles d'un réseau à
spikes ; R̂ = 0,15 signifie 15 % de spikes. Sert de point de comparaison au projet,
dont les LLM denses ont 0,00 % d'activations exactement nulles
(`docs/comparaison-spiking.md:38`, `:56-58`).

**RMSNorm (Root Mean Square Normalization)** — Normalisation qui divise par la
moyenne quadratique des activations, sans centrage : moins coûteuse que LayerNorm.
Utilisée par Qwen2, MLA et les hyper-connexions
(`docs/plan-mla-vision.md:31-34`, `reports/rapport-execution-v41.md:34`).
**Réf.** : Zhang & Sennrich, *Root Mean Square Layer Normalization*,
[arXiv:1910.07467](https://arxiv.org/abs/1910.07467).

**RoPE (Rotary Position Embedding ; plongement positionnel rotatif)** — Fait
tourner par paires les vecteurs Q et K d'un angle proportionnel à la position : la
position devient relative, sans paramètre appris. Le moteur en a deux conventions
(`NORM` et `NEOX`) et une variante retardée (voir YaRN)
(`docs/plan-mla-vision.md:38-42`, `reports/rapport-v4-couches-0-1.md:7`).
**Réf.** : Su et al., *RoFormer*, [arXiv:2104.09864](https://arxiv.org/abs/2104.09864).

**Routeur (router) · routage** — Petit réseau qui choisit, jeton par jeton, les
experts à allumer (top-k puis renormalisation). Ses conventions (fonction de score,
biais, échelle) ont chacune coûté une porte : « un faux "oui" est pire qu'un refus »
(`reports/rapport-routage-experts.md:14-32`, `docs/plan-deepseek41-complet.md:104-106`).

**RWKV (Receptance Weighted Key Value)** — Architecture récurrente alternative à
l'attention, portée dans le domaine spiking par SpikeGPT
(`docs/comparaison-spiking.md:34-40`). **Réf.** : Peng et al., *RWKV*,
[arXiv:2305.13048](https://arxiv.org/abs/2305.13048).

**SiLU · SwiGLU** — *SiLU* est une non-linéarité lisse (`x·σ(x)`), aussi appelée
sigmoid linear unit. *SwiGLU* est le bloc FFN qui combine deux projections avec
cette porte : `a = SiLU(u·x) · (v·x)`, puis `a·d` (`reports/rapport-greffon.md:12-15`).
**Où** : MLP de Qwen2, tour ViT (`clip.use_silu`), greffon `--patch`.
**Réf.** : Elfwing et al., *Sigmoid-Weighted Linear Units*,
[arXiv:1702.03118](https://arxiv.org/abs/1702.03118) ; Shazeer, *GLU Variants
Improve Transformer*, [arXiv:2002.05202](https://arxiv.org/abs/2002.05202).

**Sinkhorn (normalisation de Sinkhorn)** — Procédure itérative qui rend les lignes
**et** les colonnes d'une matrice positives de somme 1 (transport optimal
entropique). Employée 20 itérations durant par les hyper-connexions de V4.1 ;
« une HC approximative ne se voit pas — les quatre copies restent plausibles »
(`docs/plan-deepseek41-complet.md:174-186`). **Réf.** : Cuturi, *Sinkhorn
Distances*, [arXiv:1306.0895](https://arxiv.org/abs/1306.0895).

**SNN (Spiking Neural Network ; réseau de neurones à impulsions) · spike ·
neuromorphique** — Réseau dont les neurones communiquent par impulsions binaires
(0/1) au lieu de valeurs continues ; le matériel « neuromorphique » est bâti pour
ce flux d'événements. Comparaison de référence du projet avec Spikformer, SpikeGPT
et Spikingformer (`docs/comparaison-spiking.md:1-20`).
**Réf.** : Zhou et al., *Spikformer*, [arXiv:2209.15425](https://arxiv.org/abs/2209.15425) ;
Zhu et al., *SpikeGPT*, [arXiv:2302.13939](https://arxiv.org/abs/2302.13939) ;
Zhou et al., *Spikingformer*, [arXiv:2304.11954](https://arxiv.org/abs/2304.11954).

**Softmax** — Fonction qui transforme des scores en probabilités positives de
somme 1. C'est elle qui rend l'attention « dense » (toutes les clés reçoivent un
poids non nul), d'où l'intérêt des variantes sans softmax
(`docs/comparaison-spiking.md:100-106`). **Réf.** : Goodfellow, Bengio & Courville,
*Deep Learning*, chapitre 6 — [deeplearningbook.org](https://www.deeplearningbook.org/contents/mlp.html).

**Table de routage (`ffn_gate_tid2eid`)** — Variante de routage sans score : les
premières couches de V4 lisent l'expert à allumer dans une table indexée par le
jeton (`I32`, forme `[129 280 × 6]`), au lieu de calculer un score
(`reports/rapport-routage-experts.md:30-32`, `docs/plan-deepseek41-complet.md:49`).

**Tête (de sortie) · logits · argmax** — La *tête* est la matrice finale qui
projette l'état caché sur le vocabulaire ; sa sortie est un vecteur de *logits*,
et l'*argmax* en est le jeton le plus probable. Sur V4.1, la tête pèse 1,32 Go et
représente 36 % du trafic par jeton (`reports/rapport-empreinte-memoire.md:461-476`).
**Où** : `--tete-restreinte`, `--tete-garantie`.

**Tokeniser · tokenizer** — Découper le texte en jetons et l'inverse ; le
*tokenizer* est la table (vocabulaire + règles) qui fait cette conversion. Le
moteur vérifie l'aller-retour texte → jetons → texte et refuse un identifiant hors
vocabulaire (`docs/plan-deepseek-v4-flash.md:38`, `docs/convertisseur.md:276-281`).

**Top-k** — Sélection des k plus grandes valeurs d'un ensemble. Le terme apparaît
dans trois usages distincts du dépôt : les **experts** (routeur MoE), l'**attention**
(`--attn-topk`, `--qk-topk`) et la **parcimonie d'activation** (`--act-topk`,
`--topk-*` par projection). Le protocole réseau transporte les sept top-k par
projection (`docs/format-flux.md:103-109`).
**Réf.** : Fan, Lewis & Dauphin, *Hierarchical Neural Story Generation* (origine du
top-k en décodage), [arXiv:1805.04833](https://arxiv.org/abs/1805.04833).

**Transformer · couche · cachés (hidden)** — Un *transformer* est l'architecture
empilant des *couches* identiques (attention puis FFN) ; la dimension *cachée* est
la largeur du vecteur qui circule entre elles (896 pour Qwen2.5-0.5B, 5120 pour
V4.1). Le vocabulaire du dépôt compte tout en « couches × cachés × jetons »
(`docs/format-flux.md:26-31`).

**YaRN (Yet another RoPE extensioN) · mscale · facteur** — Méthode pour étendre la
portée positionnelle d'un modèle au-delà de sa longueur d'entraînement, en
interpolant les basses fréquences et en mettant le softmax à l'échelle par un
facteur `mscale = 1 + 0,1·ln(f)`. Le dépôt mesure que l'interpolation **dégrade**
sur du texte brut et que `mscale` en est la moitié nuisible : le YaRN n'est donc
appliqué qu'au-delà de 4 × la longueur déclarée (`docs/contexte-long.md:404-520`).
**Où** : `DRAVE_YARN`, `DRAVE_YARN_NON`, `DRAVE_YARN_MSCALE`.
**Réf.** : Peng et al., *YaRN*, [arXiv:2309.00071](https://arxiv.org/abs/2309.00071).

---

## 3. Formats, quantification, encodage

**b/poids (bits par poids)** — Nombre moyen de bits nécessaires pour stocker un
poids. Un modèle 8 bits coûte 8 b/poids ; le format « liste d'événements » du
dépôt en coûte 1,98, et un encodage ternaire 0,39
(`reports/rapport-optimisations.md:37`, `reports/rapport-valeur-unaire.md:89`).
C'est la mesure qui permet de comparer un format à un autre indépendamment du
nombre de paramètres.

**BitNet b1.58** — Famille de modèles **entraînés** en ternaire (−1, 0, +1), et non
quantifiés après coup ; elle tourne autour de 50-70 % de poids non nuls. Sert de
point de comparaison : « au-delà de ~90 % de zéros, un LLM généraliste s'effondre »
si l'élagage est fait après entraînement (`reports/rapport-eparsite.md:69-71`).
**Réf.** : Ma et al., *The Era of 1-bit LLMs*, [arXiv:2402.17764](https://arxiv.org/abs/2402.17764).

**Bloc de quantification · échelle par bloc** — Les poids quantifiés sont rangés
par paquets (blocs) de 32 ou 256, chacun accompagné d'une **échelle** (un facteur
multiplicatif) qui ramène les entiers dans la dynamique réelle. « Ce n'est pas le
nombre de bits qui compte, c'est la finesse des échelles » : passer d'une échelle
par vecteur à une échelle par bloc de 32 fait tomber le coût du cache KV int8 de
+7,1 % à +1,5 % de perplexité (`docs/contexte-long.md:114-149`).
**Réf.** : Frantar et al., *GPTQ*, [arXiv:2210.17323](https://arxiv.org/abs/2210.17323).

**Dequantification (déquantification)** — Recalcul de la valeur réelle d'un poids à
partir de son entier stocké et de l'échelle de son bloc : `valeur = entier ×
échelle`. C'est l'opération qui coûte du temps à chaque lecture ; la vectoriser par
quatre a fait passer l'attention à 1 M de clés de 13,6 à 7,0 ms par couche
(`docs/contexte-long.md:241-248`).

**E2M1 · E8M0** — Les deux composants du format MXFP4 : **E2M1** est la valeur sur
4 bits (1 bit de signe, 2 d'exposant, 1 de mantisse, soit les huit magnitudes
{0, ½, 1, 1½, 2, 3, 4, 6}) ; **E8M0** est l'échelle de bloc sur 1 octet, une
puissance de deux. Tous deux lus dans le fichier gpt-oss sans requantification
(`reports/rapport-passage-a-l-echelle.md:77-79`).
**Réf.** : *Microscaling Data Formats for Deep Learning*,
[arXiv:2310.10537](https://arxiv.org/abs/2310.10537).

**Échappement · indices par écarts** — Une liste d'indices triés se comprime en
n'écrivant que l'**écart** au neurone précédent, sur un octet. La valeur 255 est
*réservée* : elle annonce un indice absolu sur les deux octets suivants
(l'« échappement »). Mesuré : 99,9997 % des écarts tiennent sur un octet, et la
trace passe de 6 à 3 octets par neurone actif sans aucune perte
(`docs/format-flux.md:43-53`).

**Entropie · Huffman · inégalité de Kraft** — L'*entropie* d'une source est le
nombre minimal de bits par symbole qu'on ne peut pas battre en moyenne ; le codage
de *Huffman* s'en approche ; l'*inégalité de Kraft* (Σ2^−l ≤ 1) est la condition
qu'un code préfixe doit respecter. Le dépôt a **retiré** un gain annoncé de ×2,17
parce que le code proposé violait Kraft (Σ2^−l ≈ 1,99 > 1) — mais un rapport
continue de le citer (`reports/rapport-valeur-unaire.md:49-57`,
`reports/bilan-multi-materiel.md:92`). **Réf.** : Cover & Thomas, *Elements of
Information Theory* — cité sans lien.

**ggml · type ggml · `ggml_blck_size` · `ggml_type_size`** — ggml est la
bibliothèque de tenseurs qui sous-tend llama.cpp, et donc la définition de
référence des types quantifiés. Chaque type déclare combien de poids tient dans un
bloc (`ggml_blck_size`) et combien d'octets pèse ce bloc (`ggml_type_size`) : un
`Q4_K` range 256 poids en 144 octets. La table du moteur est **relevée**, pas
devinée, et confrontée à `libggml` (`tools/verifier_table_types.sh`,
`docs/format-clusters.md:125-158`). **Réf.** :
[ggml-common.h](https://github.com/ggml-org/ggml/blob/master/src/ggml-common.h).

**GGUF (GPT-Generated Unified Format)** — Format de fichier des modèles : un
en-tête de métadonnées (architecture, couches, tokenizer, hyper-paramètres) suivi
des tenseurs de poids, chacun avec son type de quantification. Le moteur le lit **en
place**, en plusieurs fichiers (multi-shards) ou en clusters
(`drave-core/src/gguf.rs`, `Gguf::open_multi`). **Réf.** : spécification officielle
ggml, [ggml/docs/gguf.md](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md).

**I8 · I32** — Types entiers signés du GGUF, distincts des types quantifiés. V4.1
contient deux tenseurs d'engram en `I8` (lus par déquantification générique) et
**aucun** `I32` — l'absence est vérifiée sur les deux copies du fichier
(`docs/plan-deepseek41-complet.md:71`).

**int4 · int8** — Précisions entières : 16 niveaux signés pour int4 (ou des
nibbles empaquetés), 256 pour int8. Le vocabulaire du dépôt les distingue de
`i4`/`i8` (types de stockage) et de `Q4_0`/`Q8_0` (formats ggml à échelle par
bloc). Sur le cache KV : int8 coûte +3,0 % de perplexité à 8 192 jetons, int4
+364 % (`docs/contexte-long.md:151-197`).

**IQ2_XXS · IQ1_M · IQ2_S · IQ3_XXS · IQ4_NL · IQ4_XS · IQ1_S** — Famille de types
ggml « i-quants » : des super-blocs de 256 poids à très basse précision (1 à 4
bits) utilisant des codebooks. Ce sont les formats des modèles lourds
(Kimi-K2.7 en `UD-IQ1_M`, GLM-5.3 en `UD-IQ1_S`, V4.1 en `IQ2_XXS`), et un type
absent de la table du moteur a déjà rendu un inventaire faux (8,56 Go annoncés pour
86,9 Go) (`docs/format-clusters.md:133-146`, `docs/plan-deepseek41-complet.md:71`).
**Réf.** : *QuIP#: Even Better LLM Quantization with Hadamard Incoherence and
Lattice Codebooks*, [arXiv:2402.04396](https://arxiv.org/abs/2402.04396).

**Manifeste · `mapping.tsv` · `MANIFEST.json` · `*.moe.json`** — Fichiers qui
décrivent un modèle éclaté : `mapping.tsv` relie `couche · ligne locale · expert
global · cluster` (6 144 entrées pour Qwen3-30B, volontairement en texte lisible) ;
`manifeste.json` dit le rôle de chaque fichier ; `MANIFEST.json` et `*.moe.json`
sont les formats *proposés* pour les modèles multi-shards, pas encore des fichiers
existants (`docs/format-clusters.md:31-47`, `docs/plan-modeles-lourds.md:75-82`).

**MXFP4 (Microscaling FP4 ; virgule flottante 4 bits à échelle microscopique)** —
Format 4 bits par blocs de 32, avec une échelle partagée par bloc. C'est le format
de gpt-oss-120b, lu « tel quel » par le moteur : les blocs du fichier sont les
blocs exécutés, sans copie ni requantification (`docs/convertisseur.md:26-36`,
`reports/rapport-gpt-oss-perplexite.md:6`). **Réf.** : *Microscaling Data Formats
for Deep Learning*, [arXiv:2310.10537](https://arxiv.org/abs/2310.10537).

**Nibble (quartet)** — Un demi-octet, soit 4 bits. Un poids 4 bits est un nibble ;
deux poids tiennent donc dans un octet, l'un dans les bits bas, l'autre dans les
bits hauts (`docs/convertisseur.md:26-33`).

**NVFP4** — Variante 4 bits de NVIDIA (blocs de 16 poids, échelle E4M3) présente
dans la table des types du moteur (`docs/format-clusters.md:134`).
**Réf.** : spécification OCP *Microscaling Formats (MX)* v1.0 — citée sans lien.

**PTQ (Post-Training Quantization ; quantification après entraînement)** — Réduire
la précision d'un modèle **déjà entraîné**, sans réentraînement. Tout le projet est
en PTQ — c'est précisément la limite qu'il mesure : la parcimonie ne s'impose pas,
elle s'entraîne (`reports/bilan-multi-materiel.md:86`,
`docs/programme-recherche.md:89-93`). **Réf.** : Nagel et al., *A White Paper on
Neural Network Quantization*, [arXiv:2103.13630](https://arxiv.org/abs/2103.13630).

**Q2_K · Q3_K · Q4_K · Q5_K · Q6_K · Q8_K (k-quants)** — Types ggml à
**super-blocs** de 256 poids, avec échelles et minima sur 6 bits ; `Q4_K_M` est la
quantification la plus courante des modèles publiés (Qwen3-30B, Qwen2.5-1.5B).
Un bug historique : ggml écrit les quatre quants d'un `Q6_K` en quarts successifs,
le moteur les entrelaçait — trouvé en comparant à une référence F16 des mêmes poids
(`docs/convertisseur.md:210-226`).

**Q4_0 · Q4_1 · Q5_0 · Q5_1 · Q8_0 · Q8_1** — Types ggml « legacy » à blocs de 32
poids et échelle (parfois minimum) sur 16 bits. `Q8_0` est le format de référence
du projet (tête de sortie, projections) ; `Q8_1` est le format des **activations**
chez ggml. Le moteur les lit en place, sans réencodage
(`docs/convertisseur.md:186-193`, `reports/rapport-passage-a-l-echelle.md:13`).

**QPAT** — Format du « greffon » : un en-tête `QPAT | version | couche | n | u[n] |
v[n] | d[n]` décrivant un neurone ajouté à une couche. **Où** :
`tools/make_patch.py`, `--patch` (`reports/rapport-greffon.md:19`).

**Quantification** — Stocker les poids (ou les activations, ou le cache) dans un
format plus compact que le flottant 32 bits, au prix d'une erreur. Les deux
questions du dépôt sont : *combien de bits* et *où sont les échelles* ; la seconde
compte plus que la première (`docs/vision.md:198-227`).
**Réf.** : Nagel et al., [arXiv:2103.13630](https://arxiv.org/abs/2103.13630).

**Quantification du KV** — Quantifier les clés et les valeurs du cache plutôt que
les poids. Résultat central : **tout l'écart vient des clés**, parce qu'une erreur
de clé entre dans le softmax et déplace le poids relatif d'une position entière,
alors qu'une erreur de valeur se moyenne (`docs/roadmap.md:155-194`).
**Où** : `DRAVE_KV_BITS`, `DRAVE_KV_K_F16`, `DRAVE_KV_K_F32`, `DRAVE_KV_V_F32`.

**SHA-256** — Empreinte cryptographique utilisée pour vérifier qu'un fichier
converti contient bien les mêmes octets que la source, tenseur par tenseur
(1 587 tenseurs vérifiés sur Qwen3-30B)
(`docs/format-clusters.md:60-63`). **Réf.** : FIPS 180-4,
[NIST.FIPS.180-4.pdf](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf).

**Shard (fragment)** — Un modèle trop gros pour un fichier est publié en plusieurs
**shards** : le premier porte les métadonnées et aucun tenseur, les suivants portent
les poids. DeepSeek-V4-Flash en a 3, Kimi-K2.7 8, GLM-5.3 6
(`docs/plan-deepseek-v4-flash.md:36-46`, `reports/rapport-lecteur-multifichiers.md:30`).
**Où** : `Gguf::open_multi`, `tools/lire_meta_gguf.py`.

**Super-bloc** — Unité de quantification des k-quants et des i-quants : 256 poids
partageant échelles et minima. Un tenseur quantifié se lit donc « en tranches de
256 poids », ce qui rend le découpage par expert possible quand la dimension est
multiple de 256 (`docs/format-clusters.md:50-55`,
`reports/rapport-passage-a-l-echelle.md:84-91`).

**Trinaire · deux listes · plans binaires** — Cas extrême de l'encodage : au lieu
d'écrire des valeurs, on écrit **deux listes**, celle des « + » et celle des « − »,
le signe étant porté par l'appartenance. L'information est alors dans la structure,
pas dans un octet (`docs/vision.md:211-214`, `reports/rapport-encodage.md`).
Les *plans binaires* sont la variante « 4 plans de 2 bits » et le *bitmap* la forme
1 bit/poids + signe (`reports/rapport-optimisations.md:37-38`).

**Unaire (encodage)** — Représenter une valeur en répétant une adresse autant de
fois que sa magnitude : coûteux en taille (42,45 b/poids mesurés) mais donnant un
flux d'événements naturel. Mesuré « 13,7× plus cher » que le décalage-addition
(`reports/rapport-mode-listes.md:19-24`).

**varint (entier à longueur variable)** — Entier codé sur un nombre d'octets
variable selon sa taille. Le décodeur du moteur en décode huit à la fois dans un
mot de 64 bits (technique dite SWAR) ; `reports/rapport-optimisations.md:19`,
`reports/rapport-inference.md:112`.

**zstd (Zstandard)** — Compresseur sans perte. Mesuré en étape **externe** sur la
trace : `zstd -19` fait passer la trace de 45,1 Mo à 11,1 Mo, soit −79 % au total,
sans une ligne de code dans le moteur (`reports/rapport-compacite-trace.md:20-27`).
**Réf.** : RFC 8878, [rfc-editor.org/rfc/rfc8878](https://www.rfc-editor.org/rfc/rfc8878.html).

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

## 5. Flux, protocole et transport

**Colab · notebook · tunnel** — Google Colab est un runtime distant gratuit, choisi
pour la démonstration de la phase 3.4 ; comme il n'accepte aucune connexion
entrante, il faut un tunnel (`cloudflared`, `ssh -R`, Tailscale). Le kit est dans
`colab/` (`docs/colab-reparti.md:1-21`, `:70-84`).
**Réf.** : [colab.research.google.com](https://colab.research.google.com/) ;
[tunnel Cloudflare](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/).

**Contrat d'activation (`Act`)** — L'ensemble des réglages qui changent les
chiffres calculés : niveaux de quantification, seuil, top-k, renormalisation, et les
sept top-k par projection, plus `attn_topk`, `qk_topk`, `moe_topk`. Ils **voyagent
dans l'en-tête** parce que sans eux le pair distant ne calculerait pas la même
chose — et « le client impose les siens au serveur »
(`docs/format-flux.md:100-109`, `:187`).

**Corps (payload) · en-tête** — Un message de flux = un **en-tête** de taille fixe
(79 octets en v5, `TAILLE_TETE`, verrouillé par `assert_eq!`) suivi d'un **corps**
variable. L'en-tête porte la magie, la version, le mode, la plage de couches, la
position, le compte `n`, l'échelle et le contrat d'activation ; le corps porte les
données du mode (`docs/format-flux.md:88-116`,
`docs/plan-mode4-lot-listes.md:54-55`). Un octet de trop dans l'en-tête décale tout
le corps en silence : c'est le bug le plus coûteux du chantier.

**Couche source (entrée d'attention / entrée de FFN)** — Convention d'encodage
d'une liste : un numéro de couche inférieur à 1 000 désigne l'entrée de
l'attention, supérieur ou égal à 1 000 l'entrée du FFN de la couche
`numéro − 1000`. Un seul champ porte donc deux points de trace
(`docs/format-flux.md:27-28`).

**DRVF (Drave Flux)** — Le format binaire du dépôt, à quatre usages : trace
d'exécution, rejeu, transport réseau, analyse. Un fichier commence par la magie
`DRVF` et une version (1, 2 ou 3) ; le transport utilise la même famille
d'encodage, en protocole v5 (`docs/format-flux.md:1-24`,
`docs/plan-deepseek41-complet.md:17`).

**`flux_brut` · norme finale** — Règle de responsabilité : un flux qui circule est
un **résidu brut** ; la normalisation finale n'appartient qu'au nœud qui possède la
tête de sortie, et s'applique **une fois**. Confondre « ma plage va jusqu'à la
dernière couche » et « je dois normer » a coûté la fidélité du découpage (798,3 au
lieu de 18,2) (`docs/format-flux.md:167-174`, `docs/roadmap.md:244-249`).

**Lot (mode 3) · lot en listes (mode 4)** — Le *lot* transporte `t` états d'un coup
en f32 dense, sans perte, pour que le préremplissage ne paie qu'un aller-retour par
lot (écart mesuré 0,00e0). Le *lot en listes* transporte les mêmes `t` états
encodés comme le mode 2 (échelles par bloc, valeurs i8) : 1,5 ko par jeton au lieu
de 3,5, soit **÷2,3 contre le lot dense** — le rapport de mise en œuvre écrit
« ÷2,2 » et précise que le gain n'est que de 1,07× contre le mode 2 par jeton — pour
un écart de 3,03e-2 (`docs/plan-prefill-reparti.md:1-15`,
`docs/format-flux.md:117-134`, `reports/rapport-mode4-lot-listes.md:30-35`).

**Magie (nombre magique)** — Constante en tête de fichier ou de message qui permet
de reconnaître le format : `0x44525631`, soit les octets `DRV1`, pour le protocole
de flux. Une magie absente signale une désynchronisation du flux d'octets
(`docs/format-flux.md:92`).

**Modes 0 à 4** — Les cinq modes du protocole v5 : **0** dense f32, **1** liste
quantifiée (i16 + une échelle), **2** listes à échelle par bloc (i8, écarts),
**3** lot dense, **4** lot en listes. Le mode 1 est « le format du disque, à
l'octet près » ; le mode 0 est le seul sans perte avec le mode 3
(`docs/format-flux.md:93-116`). Un mode inconnu est refusé **avant** lecture du
corps.

**Nagle · ACK différé · `TCP_NODELAY`** — Nagle est l'algorithme TCP qui retient
les petites écritures en espérant en grouper d'autres ; l'ACK différé retarde
l'accusé de réception. Ensemble, ils faisaient payer **97,6 ms par jeton** au banc
réparti au lieu de 15,9 ms de calcul ; `set_nodelay(true)` ramène l'attente à
16,1 ms (`docs/roadmap.md:113`, `docs/colab-reparti.md:30`).
**Réf.** : RFC 896, [rfc-editor.org/rfc/rfc896](https://www.rfc-editor.org/rfc/rfc896.html) ;
manuel `tcp(7)`, [man7.org](https://man7.org/linux/man-pages/man7/tcp.7.html).

**Nœud moteur · pilote · pair** — Dans la démonstration répartie, le **pilote**
garde les N premières couches (`--ppl-reparti <hôte:port> --couches-locales N`) et
le **nœud moteur** sert le reste (`--flux-serveur <port>`) ; le *pair* est
l'homologue vu par le protocole. Les deux nœuds doivent charger le **même GGUF** :
la dimension ne voyage pas (`docs/colab-reparti.md:70-102`,
`docs/format-flux.md:126-129`).

**Plafond (`PLAFOND_FLUX`, `verifier_taille`)** — Garde-fou de sûreté : toute taille
annoncée par un message est vérifiée **avant** l'allocation correspondante, contre
un plafond de 256 Mo ; un cumul est vérifié état par état. Sans lui, un en-tête
corrompu provoquerait un épuisement mémoire au lieu d'une erreur de protocole
(`docs/plan-mode4-lot-listes.md:183-232`).

**Position (compteur global de jeton)** — Champ de la trace qui compte les jetons
**globalement**, pas la place dans la fenêtre de contexte. Ce détail a coûté un
bug : avec la position dans la fenêtre, deux fenêtres réécrivaient les mêmes clés
et le rejeu rendait 356 694 au lieu de 17,43 (`docs/format-flux.md:75-86`).

**Protocole v5** — Version courante du protocole d'échange réseau : en-tête de
79 octets, cinq modes, contrat d'activation complet, refus immédiat d'un pair
incompatible en nommant les deux versions. Règle écrite dans le code : **un nouveau
mode ⇒ une nouvelle version** (`docs/format-flux.md:88-155`,
`docs/plan-mode4-lot-listes.md:150-181`).

**Sentinelle 0xFFFF** — Marque de fin facultative d'un fichier de trace
(`u16` valant 0xFFFF) ; la fin de fichier suffit, mais la sentinelle est écrite par
la version 1 (`docs/format-flux.md:35`).

**Trace de flux, versions 1 à 3** — v1 : indices `u32` + valeurs `i16` (6,02 octets
par neurone actif) ; v2 : indices par écarts `u8` + valeurs `i16` (3,01 octets, sans
perte, **défaut**) ; v3 : valeurs `i8` + échelle `f16` par bloc de 32 (≈2,08 octets
pour 21 630 645 actifs, avec perte, `DRAVE_TRACE_BLOCS=1`). Le rejeu par lots
n'accepte pas la v3, et le dit (`docs/format-flux.md:32-73`).

---

**Tranche de liste (unité d'échange)** — Granularité du contrat d'échange : un
en-tête (couche, source, échelle, bits) plus des paires (destination, valeur). La
vision en fait l'unité de travail autonome : « distribuer, c'est router des
listes » (`docs/vision.md:146-166`).

**Version (du format et du protocole)** — Trois numérotations coexistent et il faut
les distinguer : la **trace** est en version 1/2/3 (`DRAVE_TRACE_BLOCS`), le
**protocole réseau** en version 5, et le fichier GGUF a sa propre version d'en-tête.
Un refus de version est prononcé **avant** toute interprétation du corps
(`docs/format-flux.md:20-24`, `:143-153`).

## 6. Répartition, matériel et énergie

**ALM (Adaptive Logic Module)** — La brique logique élémentaire d'un FPGA Intel
(Altera) Stratix V : un petit bloc capable de réaliser une fonction combinatoire.
Le projet compte ses opérateurs en ALM : un PE d'événements tient en 176 ALM et
0 DSP, contre 115 ALM et 1 DSP avec un multiplieur
(`docs/programme-recherche.md:58`, `reports/bilan-multi-materiel.md:66-67`).
**Réf.** : documentation Intel « Stratix V Device Handbook » — citée sans lien.

**AVX2 · AVX-512 · SIMD** — *SIMD* : une instruction qui traite plusieurs nombres à
la fois. *AVX2* est le jeu d'instructions 256 bits des processeurs x86 Haswell du
banc ; le noyau de tête `Q8_0` l'utilise (`vpmaddwd` sur 32 niveaux), et la somme
entière est exacte **au bit près** (`docs/contexte-long.md:378-382`). *AVX-512* est
évoqué comme la génération qui « paierait mieux » le 4 bits
(`reports/rapport-mur-memoire-4bits.md:205`). **Réf.** : Intel Intrinsics Guide —
cité sans lien (page officielle non vérifiable depuis cette machine).

**Bande passante (bandwidth)** — Débit maximal d'un chemin de données : RAM (~20-25
Go/s), VRAM (~380-750 Go/s), DDR3 du FPGA (9,66 Go/s), PCIe x8 (6,5 Go/s), NVMe
(3,5 à 31 Go/s selon la parallélisation). C'est la ressource qui borne le décodage :
« à contexte court, tout est bande passante de poids ; à contexte long, c'est le KV
puis le préremplissage » (`docs/contexte-long.md:580-586`,
`reports/bilan-multi-materiel.md:9`).

**Cœur physique · SMT · hyperthreading · paire HT** — Un cœur *physique* exécute un
flux ; le *SMT* (hyperthreading) fait apparaître deux fils logiques par cœur en
partageant certaines ressources. Mesure du dépôt : 10 cœurs avec 20 fils
hyperthreadés donnent +27 %, mais 20 cœurs avec 40 fils ne font pas mieux que
20 cœurs (22,8 contre 22,6 Go/s) (`reports/rapport-architecture-memoire.md:249-260`,
`:163`).

**CUDA · noyau (kernel) · sm_75 · PTX · FFI** — *CUDA* est l'API de calcul GPU de
NVIDIA ; un *noyau* est la fonction exécutée massivement en parallèle ; *sm_75* est
le niveau de capacité de calcul du Quadro RTX 5000 (1024 fils par bloc, 48 ko de
mémoire partagée, pas de `__reduce_add_sync`) ; *PTX* est l'assembleur virtuel dans
lequel le noyau est précompilé et chargé par le moteur ; *FFI* est l'appel du code
Rust vers la bibliothèque C (`drave-core/gpu/drave_gpu.cu`, `gpu.rs`,
`cuda_stub.h`). **Réf.** : NVIDIA, *PTX ISA*,
[docs.nvidia.com/cuda/parallel-thread-execution](https://docs.nvidia.com/cuda/parallel-thread-execution/).

**DDR3 · DDR4** — Générations de mémoire vive externe. La carte FPGA Stratix V
embarque de la DDR3 mesurée à 9,66 Go/s, qui est **son goulot** : c'est elle qui
limite le FPGA à ~4,83 G événements/s projetés
(`reports/bilan-multi-materiel.md:9`, `docs/comparaison-spiking.md:63`). Les deux
sockets Xeon ont de la DDR4-2133 (~136 Go/s théoriques,
`reports/rapport-passage-a-l-echelle.md:152`). **Réf.** : JEDEC JESD79-3 (DDR3) —
cité sans lien.

**Débit · latence · aller-retour · TTFT** — Le *débit* est ce qui passe par
seconde (Go/s, tok/s, événements/s) ; la *latence* est le délai d'un aller-retour.
Leçon du transport réparti : « le débit ne compte pas (0,25 Mbit/s), la latence
compte quatre fois » — `attente ≈ calcul distant + 3,2 × latence`
(`docs/roadmap.md:57`). Le *TTFT* (time to first token) est le délai avant le
premier jeton généré : 74-95 ms mesurés (`reports/rapport-inference.md:83`).

**DMA (Direct Memory Access)** — Déplacement de données par le matériel sans
mobiliser le processeur ; sur cette machine, c'est le noyau qui s'en charge
(`reports/rapport-architecture-memoire.md:398`).

**DRAM-less · HMB (Host Memory Buffer)** — Un SSD *DRAM-less* n'a pas de cache
interne et emprunte un peu de RAM hôte (*HMB*) pour ses tables ; le NVMe de la
machine est un MAP1602 de ce type, ce qui explique une partie de ses performances
en lecture aléatoire (`reports/rapport-architecture-memoire.md:221`, `:285`).
**Réf.** : spécifications NVMe, [nvmexpress.org](https://nvmexpress.org/specifications/).

**DSP (Digital Signal Processor / bloc multiplieur)** — Bloc matériel spécialisé
dans la multiplication, très coûteux en surface. Le projet s'en passe comme d'un
principe (« 0 DSP ») : ses multiplications ternaires deviennent des additions et
des décalages, et le PE synthétisé tient en 176 ALM sans DSP
(`docs/histoire.md:11`, `docs/programme-recherche.md:58`, `reports/rapport-encodage.md:74`).

**Énergie par événement (nJ, pJ, TDP)** — Coût énergétique d'un événement traité :
57 nJ mesurés sur CPU, 8,3 nJ **projetés** sur FPGA (limite DDR3), ~12,7 nJ déduits
pour le GPU ; la comparaison neuromorphique cite E_AC = 0,9 pJ contre E_MAC = 4,5 pJ
sur du 45 nm (`reports/bilan-multi-materiel.md:46-48`,
`docs/comparaison-spiking.md:63`). Le *TDP* (thermal design power) est la puissance
nominale utilisée pour convertir un temps de calcul en énergie.

**FPGA (Field-Programmable Gate Array) · Stratix V · Quartus · iverilog · RTL** —
Un FPGA est un circuit dont on peut reconfigurer le câblage logique ; le projet vise
une carte Intel (Altera) **Stratix V GS « Storey Peak »**. *RTL* (register transfer
level) désigne le code Verilog qui décrit le circuit au niveau des registres et des
transferts entre eux ; *iverilog* est le simulateur libre utilisé pour vérifier,
*Quartus Prime* la chaîne de synthèse propriétaire.
Le PE et le lecteur DDR3 ont été vérifiés et synthétisés, mais le moteur complet
n'a jamais tourné sur la carte (`reports/bilan-multi-materiel.md:22-27`,
`docs/roadmap.md:71-81`). **Réf.** : [iverilog](https://steveicarus.github.io/iverilog/) ;
Quartus Prime et Stratix V — documentations Intel citées sans lien.

**GPU · Quadro RTX 5000 · miroir VRAM · déport** — Les deux Quadro RTX 5000 (16 Go
chacune) servent de *déport* : le cache KV y est recopié en **miroir** paginé, ce
qui fait passer l'attention à 1 M de clés de 968 ms à 13,2 ms par couche (×73) et
rend le poste « attention » plat (3,3 ms/jeton) au lieu de croître linéairement
(`docs/contexte-long.md:212-297`). **Où** : `DRAVE_GPU`, `DRAVE_GPU_KV`,
`DRAVE_GPU_TETE`, `DRAVE_GPU_TOPK`, `DRAVE_GPU_EXPERTS`.

**Grandes pages · TLB · alignement 2 Mo** — Le *TLB* est le cache des traductions
d'adresses mémoire ; chaque page manquée coûte une marche de table. Des pages de
2 Mo au lieu de 4 ko divisent ce coût par 512, et l'alignement à 2 Mo du conteneur
proposé prépare leur usage (`reports/rapport-passage-a-l-echelle.md:160`,
`docs/convertisseur.md:146-148`).

**Grappe · `commun.gguf` · `cluster-XX.gguf`** — Forme éclatée d'un modèle :
`commun.gguf` porte embeddings, tête, attention, normes et **routeurs**, chaque
`cluster-XX.gguf` porte les tranches d'experts d'une grappe, et `mapping.tsv` relie
les deux. Un nœud qui ne sert que la grappe 0 charge 3,20 Go au lieu de 18,56 et
625 ms au lieu de 3,9 s (`docs/format-clusters.md:1-13`, `:78-89`).
**Où** : `tools/convertir_clusters.py`, `DRAVE_CLUSTERS`.

**L1 · L2 · ligne de cache · banque mémoire** — Mémoires internes du processeur, du
plus rapide (L1, quelques dizaines de Kio) au plus grand (L2 partagé, 256 Kio ici).
L'accumulateur du mode push doit tenir en L1 sous peine de s'effondrer ; les
banques mémoire imposent un rembourrage des tuiles transposées, sans quoi 32 voies
d'une lecture tombent dans la même banque (`reports/bilan-multi-materiel.md:132`,
`docs/contexte-long.md:219-224`).

**M20K** — Bloc de mémoire embarqué du FPGA Stratix V (20 kbit). L'accumulateur
d'un PE (4 096 × 24 bits = 12 Kio) tient dans les M20K ; la collecte irrégulière
des listes en consomme 41 % (`reports/rapport-cpu-aer.md:11`,
`reports/bilan-multi-materiel.md:95`).

**MAC (Multiply-Accumulate) · AC (Accumulate)** — *MAC* : une multiplication suivie
d'une addition, l'opération de base d'un réseau dense. *AC* : la seule addition,
suffisante quand les valeurs sont binaires — c'est l'économie des réseaux à spikes
et du ternaire (`docs/comparaison-spiking.md:59`). Une carte FPGA fournit ~312
voies de MAC, soit ~9 400 ALM (`reports/rapport-minimal.md:80-81`).

**mmap (memory-mapped file) · `madvise` · `DRAVE_MMAP`** — *mmap* projette un
fichier en mémoire : le noyau lit les pages à la demande au lieu de charger le
fichier. C'est ce qui permet d'ouvrir un GGUF de 365,7 Go avec 47 Mo de mémoire
résidente ; `DRAVE_MMAP=0` revient à `read_to_end`, qui duplique le modèle (9,32 s
et 6,35 Go contre 30,68 s et 19,20 Go en clusters)
(`docs/format-clusters.md:181-186`, `reports/rapport-architecture-memoire.md:372-376`).
`madvise(MADV_WILLNEED)` demande la prélecture, sans gain mesuré ici.
**Réf.** : [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html),
[madvise(2)](https://man7.org/linux/man-pages/man2/madvise.2.html).

**NUMA (Non-Uniform Memory Access) · nœud · UPI/QPI · premier-touch · `--pin`** —
Sur une machine bi-socket, chaque processeur a sa mémoire proche (*nœud NUMA*) et
les accès croisés passent par un lien inter-socket (*UPI* chez Intel, *QPI* chez
d'autres). Le *premier-touch* est la règle qui alloue une page sur le nœud du fil
qui l'écrit. Gain au banc : 20,7 → 24,7 Go/s ; mais sur la charge réelle,
l'épinglage `--pin` est une **perte** (23,2 → 27,6 s) — l'ordonnanceur fait mieux
seul (`docs/convertisseur.md:99-109`, `:236-242`).
**Réf.** : documentation noyau Linux, [docs.kernel.org/mm/numa.html](https://docs.kernel.org/mm/numa.html).

**Nœud partiel** — Nœud qui ne charge qu'une partie des grappes
(`DRAVE_CLUSTERS=0,3`) au lieu du modèle entier. Un cluster **demandé mais absent du
disque est une erreur**, pas un silence ; et rien n'additionne encore les
contributions de deux nœuds partiels (`docs/format-clusters.md:160-178`,
`reports/rapport-lecteur-multifichiers.md:125`).

**NVLink** — Lien direct entre cartes NVIDIA, mesuré à 25,78 Go/s ici, soit ~2× le
PCIe réel ; `cudaMemcpy` l'emprunte automatiquement
(`docs/convertisseur.md:95`, `reports/rapport-architecture-memoire.md:226`).

**NVMe · SSD · `O_DIRECT` · `pread`** — *NVMe* est le protocole des SSD rapides
branchés en PCIe ; *pread* lit à une position donnée sans déplacer le curseur ;
*O_DIRECT* demande à contourner le cache du noyau (il échoue ici, errno 29). Le
NVMe parallélisé à 16 lecteurs (31 Go/s) dépasse la RAM (22 Go/s) : c'est le chemin
retenu pour les experts (`reports/rapport-architecture-memoire.md:181-195`).
**Réf.** : [pread(2)](https://man7.org/linux/man-pages/man2/pread.2.html).

**PCIe (Peripheral Component Interconnect Express)** — Bus qui relie les cartes
d'extension. Mesuré à 6,5 Go/s en x8 Gen3 ici ; c'est **le goulot d'un montage
hybride** : envoyer un flux d'événements au GPU coûte plus cher que de le calculer
sur CPU tant que celui-ci tient 5,3 G événements/s (~10,6 Go/s d'événements), donc
« le seuil d'intérêt du GPU par PCIe est proche de 1 »
(`docs/convertisseur.md:85-109`). **Réf.** : PCI-SIG — cité sans lien.

**PE (Processing Element ; élément de calcul)** — L'unité qui traite un événement
par cycle dans le FPGA. Le dépôt en dimensionne le nombre selon la DDR3 : 51 voies
tiennent la carte, l'optimum du banc seul est 32 PE à 177 MHz
(`reports/bilan-multi-materiel.md:55`, `reports/rapport-cpu-aer.md:11`).

**QSFP+** — Lien réseau 4,8 Go/s envisagé pour chaîner plusieurs cartes FPGA
(`reports/bilan-multi-materiel.md:9`, `docs/convertisseur.md:94`).
**Réf.** : spécifications SFF, [snia.org](https://www.snia.org/technology-communities/sff/specifications).

**RAM · VRAM · RSS** — *RAM* : mémoire de l'hôte (125 Go ici) ; *VRAM* : mémoire des
cartes graphiques (2 × 16 Go, 30,2 Go exploitables) ; *RSS* (resident set size) :
mémoire réellement occupée par un processus. Le contraste qui résume le projet :
**47 Mo de RSS pour 365,7 Go de modèle adressé** en `mmap`
(`reports/rapport-architecture-memoire.md:370-376`).
**Réf.** : [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html).

**Roofline** — Modèle qui prédit si un calcul est borné par la puissance de calcul
ou par la bande passante mémoire ; le dépôt l'utilise pour projeter un modèle sur
un matériel donné (`src/roofline.py`, `docs/programme-recherche.md:11`).
**Réf.** : Williams, Waterman & Patterson, *Roofline: An Insightful Visual
Performance Model*, Communications of the ACM, 2009 — cité sans lien.

**USB** — Seul lien effectivement configuré du Stratix V dans le relevé matériel
(625 Mo/s), cinquante fois moins que le NVMe parallélisé — ce qui interdit d'y
déléguer le calcul (`reports/rapport-architecture-memoire.md:385-397`).

**Xeon E5-2687W v3 · CPU** — Le processeur du banc : 2 sockets × 10 cœurs (40 fils
logiques), 125 Go de RAM, jeu d'instructions AVX2. Toutes les mesures « CPU » du
dépôt sont faites dessus (`reports/bilan-multi-materiel.md:7`,
`reports/rapport-inference.md:5`).

---

## 7. Mesure, qualité et méthode expérimentale

**Amplification chaotique** — Explication d'un écart de continuation entre deux
chemins de calcul pourtant à perplexité identique : une différence de 1e-5 sur un
logit peut faire basculer l'`argmax`, et la suite diverge. « La perplexité est
identique, pas la continuation » (`docs/contexte-long.md:315-318`,
`reports/rapport-aiguille-topk.md:136-139`).

**Banc dégénéré · « un banc qui passe ne prouve pas qu'il mesure »** — Un banc dont
les données rendent le résultat vrai pour de mauvaises raisons. Exemple consigné :
un banc de scores GPU où toutes les positions partageaient la même clé, ce qui a
donné 1,03e-7 au lieu de 1,60-2,25e-7 (`reports/rapport-gpu-scores.md:27-36`,
`docs/sprints.md:69-73`).

**Cohérence des documents (audits)** — Trois rapports passent le corpus au crible et
classent chaque affirmation en OK / PÉRIMÉ / CONTRADICTOIRE / MANQUANT, avec
`fichier:ligne` : `reports/rapport-coherence-docs.md` (80 affirmations, 38
périmées), `reports/rapport-coherence-docs-2.md` (66 affirmations, 27 tiennent) et
`reports/rapport-coherence-vision.md` (les 18 documents de `docs/`).
**Où** : à lire avant de citer un chiffre ancien.

**Corrélation · différence symétrique · accord top-1** — Trois façons de comparer
deux exécutions : la *corrélation* des logits (0,999024 entre le moteur et
llama.cpp sur GLM-5.3), la *différence symétrique* des ensembles retenus (0 sur
14/14 lignes pour le top-k GPU), l'*accord top-1* (497 jetons sur 511 gardent le
même argmax) (`reports/rapport-mla-experts.md:106-113`,
`reports/rapport-logits-gpu-vs-cpu.md:40-44`).

**Croisement push/pull (≈22 %)** — La densité d'activation à laquelle le coût des
deux chemins s'égale : en dessous, le push gagne (×2,1 à 10 %, ×8,3 à 1 %) ;
au-dessus, le dense gagne (×4,7 à 100 %). Le seuil `seuil_push` a été corrigé de
0,15 à **0,22** après une première campagne fausse
(`reports/rapport-croisement-push-pull.md:43-48`,
`reports/rapport-mur-memoire-4bits.md:53-57`).

**Densité d'activation · sparsité · parcimonie · creux** — Fraction des neurones
dont l'activation n'est pas nulle (ou dépasse un seuil). Le projet mesure 17,9 % à
seuil 5 % du max sur Qwen2.5-0.5B, et 100 % (aucun zéro exact) à seuil nul ; c'est
cette densité qui décide du chemin d'exécution
(`docs/vision.md:44-55`, `reports/rapport-localite-activation.md:43-47`).
La densité **par couche** varie de 20 % à 56 %, donc la décision push/pull est une
propriété de la couche, pas du modèle (`docs/roadmap.md:28`).

**Diff par couche** — Comparaison de deux traces couche par couche, jeton par jeton,
pour localiser une divergence au lieu de la constater : « KV f32 contre int8 →
première divergence couche 1, jeton 0, couche la plus touchée FFN 2 »
(`docs/roadmap.md:16`, `tools/diff_flux.py`).

**Écart relatif · RMS · écart max** — Façons de chiffrer une erreur. L'*écart max
relatif* est utilisé pour comparer des tenseurs (1e-7, 5,2e-7, 1,8e-6) ; le *RMS*
(root mean square) pour une erreur répartie (0,085 % du max de la liste pour la
trace v3) ; la *tolérance* du dépôt pour un noyau GPU est 1e-6
(`docs/format-flux.md:62-65`, `reports/rapport-gpu-scores.md:50-52`).

**Fidélité (bit à bit · exact · équivalent)** — Trois niveaux définis par le dépôt :
*bit à bit* (même forme d'exécution, même résultat), *exact* (aucun réencodage : les
octets du fichier sont ceux exécutés), *équivalent* (même perplexité à l'arrondi
près). Un convertisseur qui réencode doit prouver « exact » ou renoncer au nom
« haute fidélité » (`docs/convertisseur.md:150-163`).

**Gini · Jaccard · η² · R² · r · exposant de Heaps** — Statistiques employées pour
tester une hypothèse : le *Gini* mesure la concentration d'un routage d'experts par
couche ; le *Jaccard* le recouvrement de deux ensembles d'experts ; *η²* et *R²* la
part de variance expliquée ; *r* une corrélation ; l'*exposant de Heaps* (~0,21) la
croissance du vocabulaire d'un corpus. Ce sont eux qui ont infirmé la piste des
« motifs d'expertise » (R² hors échantillon = +0,007)
(`reports/rapport-empreinte-memoire.md:114`, `reports/rapport-programme-evolutif.md:36-42`).

**Localité d'activation · réorganisation contiguë** — Les neurones qui s'allument
ensemble sont-ils voisins en mémoire ? Un élagage *contigu* est 30 % plus rapide
qu'un élagage *dispersé* à taux égal, et grouper les neurones co-actifs est la
piste de gain la plus proche du programme (`reports/rapport-inference.md:285-288`,
`docs/programme-recherche.md:219-221`).

**Magnitude · quantile · « top 10 % »** — La *magnitude* est la valeur absolue
d'une activation ; le *quantile* Q d'une trace est le seuil qui retient une fraction
donnée. Mesure clé du projet : les 10 % de neurones les plus forts portent **33,1 %**
de la magnitude, et seuls **0,08 %** sont « chauds » plus de 90 % du temps — donc un
préchargement statique ne paie pas (`docs/vision.md:79-81`,
`reports/rapport-localite-activation.md:43-47`).

**Moindres carrés · span linéaire · monômes quadratiques · rang effectif · valeur
singulière** — Outils de l'étape d'apprentissage sans rétropropagation :
*moindres carrés* pour ajuster une lecture sur le journal, *span linéaire* pour
savoir si une direction est déjà dans l'espace des poids, *monômes quadratiques*
(401 856 produits `x_i·x_j`) comme candidats non linéaires, *rang effectif* et
*valeurs singulières* pour mesurer la saturation d'une projection. Conclusion
mesurée : un nœud linéaire ne peut rien ajouter à 69,2 % des poids
(`docs/programme-recherche.md:123-127`, `reports/rapport-capteur-hebbien.md:44-92`).

**p50 · p90 · p95 · médiane · max** — Quantiles d'une distribution d'écarts :
« |ΔNLL| médian 0,076, max 1,49 », « p90 0,0017 ». Le dépôt préfère la médiane et le
p90 au maximum seul, parce qu'un jeton atypique peut porter tout l'écart
(`reports/rapport-gpt-oss-perplexite.md:76`, `reports/rapport-aiguille-topk.md:133`).

**Porte de format** — Vérification que chaque type quantifié est déquantifié
correctement, comparé à `libggml` au bit près : « 19 formats lisibles, 17 à la
porte » (`tools/portes_formats.sh`, `docs/format-clusters.md:148-158`,
`reports/rapport-coherence-vision.md:145-146`).

**Profilage par neurone · `--ppl-profil`** — Compter quels neurones s'allument, à
quelle fréquence, avec quelle magnitude, couche par couche (`--profil-neurones`,
`--neurones-sortie`) ; le temps par poste, lui, s'imprime à chaque `--ppl` (pas de
drapeau), et `--ppl-profil` ajoute la **perte par tranche de 256 positions**. C'est l'axe 1
de la vision : « un flux de listes est observable par construction »
(`docs/vision.md:62-89`, `docs/roadmap.md:129-149`).

**Profondeur de sonde · fenêtre · taux de récupération** — Vocabulaire du test de
l'aiguille : le code à retrouver est planté à une *profondeur* relative (0,1 = tout
au début, 0,9 = tout à la fin), chaque essai est une *sonde*, et le *taux de
récupération* est la fraction de sondes réussies. La perplexité ne dit pas si le
modèle **retrouve** une information : c'est pourquoi ce test existe
(`docs/contexte-long.md:533-550`, `reports/rapport-aiguille.md:74`).

**Référence indépendante (numpy)** — Seconde implémentation de la **même formule**,
écrite dans un autre langage, pour valider un chemin : « une seconde implémentation
de la même formule, pas une seconde exécution de la même implémentation ». C'est
ainsi que MLA (5,2e-7), les patchs de vision (5,4e-7) et le projecteur (1,7e-6) ont
été validés (`docs/vision.md:182-190`, `docs/plan-mla-vision.md:8-16`,
`src/transformer_np.py`).

**Reproduit · non reproduit** — Mention explicite du dépôt quand un chiffre n'a pas
été re-mesuré depuis sa première publication : « valeurs du 30/09, non reproduites
depuis : seul l'écart A/B fait foi » (`docs/contexte-long.md:565-567`,
`docs/plan-gpu-topk.md:86-90`). Un chiffre « non reproduit » ne doit pas être cité
comme acquis.

**Seuil absolu · seuil relatif** — Un seuil *absolu* coupe les activations sous une
valeur fixe ; un seuil *relatif* les coupe sous une fraction du maximum du vecteur.
Mesure : le seuil absolu est **10× moins efficace** que le k-WTA à sparsité égale
(`reports/rapport-parcimonie-imposee.md:47`, `docs/roadmap.md:139-141`).

**Test de l'aiguille (« l'aiguille dans la botte de foin »)** — Banc de
récupération : on plante un code (`AZUR-7391`) dans un long remplissage et on
vérifie que le modèle le ressort. Version 2 : remplissage Wikitext-2, réponses de
40 jetons, préremplissage par lots — **12 sondes sur 12** trouvées
(`docs/contexte-long.md:533-550`, `reports/rapport-aiguille.md:74`,
`tools/aiguille.py`). **Réf.** : Hsieh et al., *RULER: What's the Real Context Size
of Your Long-Context Language Models?*, [arXiv:2404.06654](https://arxiv.org/abs/2404.06654).

**Trace · mesure · recalcul** — Distinction de méthode : une trace est un
enregistrement, une mesure est un chiffre obtenu en exécutant, un recalcul est une
conséquence arithmétique du code. L'audit prévient : « les chiffres recalculables
(3 663, 917 583, 1 419) sont des conséquences arithmétiques du code, pas des mesures
neuves » (`reports/rapport-coherence-docs.md:205-211`).

---

## 8. Points relevés, non corrigés

Ces points ont été croisés en rédigeant ce glossaire. **Aucun autre fichier n'a été
modifié** : ils sont listés ici, avec leur chemin et leur citation, pour qu'un
lecteur ne s'y trompe pas.

1. **L'attribution de l'écart int8 se contredit dans le même document.**
   `docs/contexte-long.md:399-401` : « L'écart de +3,0 % contre +0,8 % à 8 192 vient
   donc d'ailleurs : probablement la quantification des VALEURS et la précision du
   softmax, pas l'arrondi des clés. » — alors que le §4.bis.3 du même fichier
   (`:176-197`) et `docs/roadmap.md:30` concluent l'inverse : « tout l'écart est
   dans les CLÉS ».

2. **Un paragraphe barré « CORRIGÉ » subsiste au milieu d'une section.**
   `docs/contexte-long.md:241-248` : « ~~Le format ne change presque rien au temps
   GPU (13,2 à 15,0 ms à 1 M) : le noyau est borné par la déquantification
   scalaire.~~ **CORRIGÉ** ». La phrase fausse reste lisible ; la valeur corrigée
   est 6,5-7,4 ms.

3. **Les phases P1 à P5 du plan V4.1 sont écrites deux fois.**
   `docs/plan-deepseek41-complet.md` porte deux titres « P1 », deux « P2 », deux
   « P3 », deux « P4 », deux « P5 » : une version « **FAIT** (02/10) » (`:164-169`)
   suivie de la version « à faire » (`:171-186`). Le statut se contredit à la
   lecture linéaire.

4. **Le mode 4 est dit « à écrire » alors qu'il est mesuré.**
   `docs/plan-prefill-reparti.md:421` : « **Le lot en listes** : c'est le mode 4, à
   écrire quand le débit gênera. » — contredit par `docs/format-flux.md:88-125` et
   `docs/plan-mode4-lot-listes.md:6` (« L'implémentation est faite »). Le préambule
   (`:3-11`) prévient que le corps du plan n'est pas réécrit, mais la phrase reste
   fausse telle quelle.

5. **Deux perplexités « clusters » sans rappel du contexte.**
   `docs/format-clusters.md:116` : « origine 15,2789 · clusters 15,2789 (mêmes
   63 jetons) » ; `docs/format-clusters.md:167-173` : « 8 | **799,8557** »
   (mêmes 7 jetons). 799,8557 est aussi la porte de non-régression citée partout
   (`docs/sprints.md:39`) : le lecteur qui ne voit qu'un des deux chiffres croit à
   une contradiction.

6. **Le bandeau de statut casse le tableau des modèles lourds.**
   `docs/plan-modeles-lourds.md:23-29` insère un bloc « Où en est ce plan (02/10) »
   entre la ligne d'en-tête (`:20-21`) et les lignes de données (`:30-38`) : le
   tableau n'a plus d'en-tête, et les colonnes ne sont plus lisibles.

7. **Trois durées par jeton pour le même modèle.**
   `docs/plan-modeles-lourds.md:92` : « ~73 s/jeton » (Kimi-K2.7) ;
   `reports/rapport-mla-experts.md:110` : « **53 s par jeton** » ;
   `reports/rapport-mla-experts.md:236` : « le moteur met ~190 s par jeton ». Aucune
   datation ne permet de savoir laquelle fait foi.

8. **Une affirmation que le corpus qualifie lui-même de fausse est reprise.**
   `reports/bilan-multi-materiel.md:96` : « il est **8 % plus rapide** que le dense
   (15,8 contre 14,7 tok/s) » — or `reports/rapport-croisement-push-pull.md:66-71`
   écrit : « **C'est faux, et je l'ai mesuré deux fois** », le pull corrigé valant
   **36,4 tok/s**.

9. **Le croisement push/pull est donné à deux densités différentes.**
   `reports/rapport-analyse-flux.md:14` : « Le croisement push/pull du projet est
   mesuré à **~10 % de densité** » — contredit par
   `reports/rapport-croisement-push-pull.md:43` : « Les deux architectures se
   croisent à **~22 % de densité d'activation**, pas à 10 % », et par
   `docs/vision.md:44-46`.

10. **Une accuracy de 4 971 % dans un tableau.**
    `reports/rapport-encodage.md:42` : « | 2.00 | **4971.00 %** | 5.5 | dense
    ternaire (référence CDC) | » — une exactitude supérieure à 100 % est impossible
    (49,71 % attendu, cf. `reports/rapport-minimal.md:12`).

11. **Le `mmap` est annoncé « pas fait » dans un rapport qui le dit fait ailleurs.**
    `reports/rapport-lecteur-multifichiers.md:267-268` : « Le **mmap** :
    `read_to_end` charge tout le fichier. DeepSeek-V4.1-Flash fait 366 Go, il
    restera hors de portée sans lui. » — contredit par `:171-186` du même fichier
    (« Les fichiers sont maintenant **mappés** », 9,32 s / 6,35 Go) et par
    `docs/format-clusters.md:181-186`.

12. **Le top-k GPU est dit « pas encore branché » après avoir été branché.**
    `reports/rapport-gpu-topk-selection.md:347-349` : « Le top-k GPU n'est donc
    **pas encore branché dans le moteur** [...] jusqu'à l'étape 3. » — contredit par
    `:164-171` du même rapport (« ✅ **fait** (opt-in `DRAVE_GPU_TOPK=1`) ») et par
    `docs/plan-gpu-topk.md:99`.

13. **Un état « reste à faire » survit à l'état « fait » dans le plan MLA.**
    `docs/plan-mla-vision.md:104-106` : « Ce qui reste : **le chemin MLA dans le
    moteur** » — alors que la section précédente (`:55-72`) annonce « MLA EST FAIT
    ET VALIDÉ ». Les sections d'états successifs cohabitent sans être datées.

14. **Une valeur non reproduite est citée comme un acquis dans la vision.**
    `docs/vision.md:82-86` cite `--attn-topk 256` : « 234,88 contre 298,56 » ;
    `docs/contexte-long.md:565-567` précise que ces valeurs « ne sortent pas du
    binaire courant » et que « seul l'écart A/B fait foi », et
    `docs/plan-gpu-topk.md:86-90` ajoute qu'elles « n'[ont] pas été reproduite[s]
    depuis ».

15. **Des mesures de dispersion manifestement fausses restent dans un rapport.**
    `reports/rapport-cpu-aer.md:17-18` : « dispersion (`np.bincount`) :
    **183999808.87 G événements/s** » et « **364797216.41 G** » — soit ~1,8·10¹⁷
    événements/s, incompatibles avec les 18,1 G événements/s du GPU ; le rapport
    signale lui-même (`:62-65`) que ces chiffres ne sont pas exploitables.

16. **Le coût de la journalisation est donné pour deux artefacts différents.**
    `docs/programme-recherche.md:29` : « Journaliser les listes d'activations
    (1,2 Mo/token, **+3,0 %**) » — le +3,0 % est celui du **capteur hebbien**
    (`reports/rapport-programme-evolutif.md:17`), tandis que la trace de flux coûte
    **+8 % de temps** et 258 ko/jeton (`docs/roadmap.md:15`). Les deux chiffres sont
    exacts séparément, mais la phrase les associe au même objet.

17. **Le périmètre annoncé ne correspond pas au disque.**
    La demande de glossaire décrit « une centaine de rapports » dans `reports/` ;
    le dossier en contient **60** (plus 9 fichiers dans `sprints/`). Les 18
    documents de `docs/` sont, eux, exacts (`reports/rapport-coherence-vision.md:3`
    parle aussi de « 18 documents »).

18. **Des termes attendus sont absents du corpus.**
    `Hadamard`, `MTP` (hors la mention `dspark_*`), `SparseVec` hors des rapports
    d'optimisation, `speculative decoding` en toutes lettres, `MTok/s`, `Gbit/s`,
    `p50/p95` (seul p90 apparaît) ne figurent **pas** dans `docs/` ni dans
    `reports/`. `MTP` n'apparaît que dans `journal/sessions/.../rapport.md:2545`
    (« MTP | `dspark` : 128 experts top-3 sur les couches 37-39 »), fichier hors du
    périmètre de ce glossaire. Les entrées correspondantes ci-dessus sont donc
    explicitées comme telles.

19. **Un drapeau présenté comme existant n'existe pas.**
    `docs/vision.md:74` liste, dans le tableau « Ce qui existe déjà, et qui a
    servi » : « `--ppl-profil` | le temps par poste (projections, rope, attention,
    FFN, tête) » — et `docs/contexte-long.md:520` s'appuie dessus. Or
    `reports/rapport-drapeaux-ignores.md:97` classe déjà ce drapeau « **jamais
    lu** », et le code courant ne le reconnaît pas : il reste un champ mort
    (`drave-core/src/main.rs:541`, jamais alimenté par `analyser()`), donc tout
    usage est traité comme drapeau inconnu.

20. **Un drapeau dit inexistant existe désormais.**
    `reports/rapport-drapeaux-ignores.md:196-198` recommande `--options-actives`
    « (et `--options-strict`) » tout en précisant ailleurs que la variante
    `--options-strict` **n'existe pas** ; l'arbre courant l'implémente pourtant
    (`drave-core/src/main.rs:619`). Le rapport est daté du 30/09 : toute citation
    croisée doit être datée.

21. **Un rapport de sprint déclare « aucun poids ouvert » pour un modèle que le
    dépôt télécharge.** `sprints/07-cloture-de-la-nuit.md:138-142` :
    « **DeepSeek-V4.1-Flash est un modèle d'API** … **aucun poids ouvert**, donc
    rien à télécharger » — contredit par `tools/manifeste_modeles_lourds.json`
    (entrée `DeepSeek-V4.1-Flash-Q2`, 365,7 Go), par `tools/portes_formats.sh:38`
    et par `sprints/09:5`. `sprints/` est hors du périmètre initial de ce
    glossaire, mais le fichier est dans le dépôt et la contradiction est frontale.

---

## 9. Sources externes citées

Articles et spécifications, par ordre d'apparition dans le glossaire. Toutes les
adresses de cette liste ont été testées (réponse HTTP 200) ; les documents que je
n'ai pas pu vérifier sont cités **par leur titre, sans lien**.

- Vaswani et al., *Attention Is All You Need* — <https://arxiv.org/abs/1706.03762>
- Ioffe & Szegedy, *Batch Normalization* — <https://arxiv.org/abs/1502.03167>
- Sennrich et al., *Neural Machine Translation of Rare Words with Subword Units* — <https://arxiv.org/abs/1508.07909>
- Jiang et al., *Mistral 7B* — <https://arxiv.org/abs/2310.06825>
- Hendrycks & Gimpel, *Gaussian Error Linear Units* — <https://arxiv.org/abs/1606.08415>
- Ainslie et al., *GQA: Training Generalized Multi-Query Transformer Models* — <https://arxiv.org/abs/2305.13245>
- Ba, Kiros & Hinton, *Layer Normalization* — <https://arxiv.org/abs/1607.06450>
- Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* — <https://arxiv.org/abs/2106.09685>
- Liu et al., *Lost in the Middle* — <https://arxiv.org/abs/2307.03172>
- DeepSeek-AI, *DeepSeek-V2* (MLA) — <https://arxiv.org/abs/2405.04434>
- Fedus, Zoph & Shazeer, *Switch Transformers* — <https://arxiv.org/abs/2101.03961>
- Shazeer, *Fast Transformer Decoding: One Write-Head is All You Need* — <https://arxiv.org/abs/1911.02150>
- Qwen Team, *Qwen2.5-VL Technical Report* — <https://arxiv.org/abs/2502.13923>
- DeepSeek-AI, *DeepSeek-V3 Technical Report* (MTP) — <https://arxiv.org/abs/2412.19437>
- Leviathan et al., *Fast Inference from Transformers via Speculative Decoding* — <https://arxiv.org/abs/2211.17192>
- Goodfellow, Bengio & Courville, *Deep Learning* — <https://www.deeplearningbook.org/contents/ml.html> et <https://www.deeplearningbook.org/contents/mlp.html>
- Brown et al., *An Estimate of an Upper Bound for the Entropy of English* — <https://aclanthology.org/J92-1002/>
- Xiao et al., *Efficient Streaming Language Models with Attention Sinks* — <https://arxiv.org/abs/2309.17453>
- Zhang & Sennrich, *Root Mean Square Layer Normalization* — <https://arxiv.org/abs/1910.07467>
- Su et al., *RoFormer* (RoPE) — <https://arxiv.org/abs/2104.09864>
- Peng et al., *RWKV* — <https://arxiv.org/abs/2305.13048>
- Elfwing et al., *Sigmoid-Weighted Linear Units* — <https://arxiv.org/abs/1702.03118>
- Shazeer, *GLU Variants Improve Transformer* — <https://arxiv.org/abs/2002.05202>
- Cuturi, *Sinkhorn Distances* — <https://arxiv.org/abs/1306.0895>
- Zhou et al., *Spikformer* — <https://arxiv.org/abs/2209.15425>
- Zhu et al., *SpikeGPT* — <https://arxiv.org/abs/2302.13939>
- Zhou et al., *Spikingformer* — <https://arxiv.org/abs/2304.11954>
- Fan, Lewis & Dauphin, *Hierarchical Neural Story Generation* (top-k) — <https://arxiv.org/abs/1805.04833>
- Peng et al., *YaRN* — <https://arxiv.org/abs/2309.00071>
- Ma et al., *The Era of 1-bit LLMs* (BitNet b1.58) — <https://arxiv.org/abs/2402.17764>
- Frantar et al., *GPTQ* — <https://arxiv.org/abs/2210.17323>
- *Microscaling Data Formats for Deep Learning* (MXFP4, E2M1/E8M0) — <https://arxiv.org/abs/2310.10537>
- Nagel et al., *A White Paper on Neural Network Quantization* — <https://arxiv.org/abs/2103.13630>
- *QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks* (i-quants) — <https://arxiv.org/abs/2402.04396>
- Dosovitskiy et al., *An Image is Worth 16x16 Words* (ViT) — <https://arxiv.org/abs/2010.11929>
- Radford et al., *CLIP* — <https://arxiv.org/abs/2103.00020>
- Pope et al., *Efficiently Scaling Transformer Inference* (KV, préremplissage) — <https://arxiv.org/abs/2211.05102>
- Hsieh et al., *RULER* — <https://arxiv.org/abs/2404.06654>
- ggml, spécification GGUF — <https://github.com/ggml-org/ggml/blob/master/docs/gguf.md>
- ggml, définitions des types quantifiés — <https://github.com/ggml-org/ggml/blob/master/src/ggml-common.h>
- llama.cpp (référence de correction) — <https://github.com/ggml-org/llama.cpp>
- RFC 8878, *Zstandard Compression* — <https://www.rfc-editor.org/rfc/rfc8878.html>
- RFC 896, *Congestion Control in IP/TCP Internetworks* (Nagle) — <https://www.rfc-editor.org/rfc/rfc896.html>
- manuels Linux `mmap(2)`, `madvise(2)`, `pread(2)`, `proc(5)`, `tcp(7)` — <https://man7.org/linux/man-pages/man2/mmap.2.html>, <https://man7.org/linux/man-pages/man2/madvise.2.html>, <https://man7.org/linux/man-pages/man2/pread.2.html>, <https://man7.org/linux/man-pages/man5/proc.5.html>, <https://man7.org/linux/man-pages/man7/tcp.7.html>
- Noyau Linux, documentation NUMA — <https://docs.kernel.org/mm/numa.html>
- NVIDIA, *PTX ISA* — <https://docs.nvidia.com/cuda/parallel-thread-execution/>
- FIPS 180-4 (SHA-256) — <https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf>
- Icarus Verilog — <https://steveicarus.github.io/iverilog/>
- OpenBLAS — <https://www.openblas.net/>
- NumPy — <https://numpy.org/doc/stable/>
- SFF (QSFP+) — <https://www.snia.org/technology-communities/sff/specifications>
- NVMe — <https://nvmexpress.org/specifications/>
- Hugging Face, Xet — <https://huggingface.co/docs/hub/xet/index>
- Google Colab — <https://colab.research.google.com/>

Cités **par titre, sans lien** (adresse non vérifiable depuis cette machine, ou
document non public) : Lazzaro et al., *Silicon auditory processors as computer
peripherals* ; Gerstner & Kistler, *Spiking Neuron Models* ; Cover & Thomas,
*Elements of Information Theory* ; Warren, *Hacker's Delight* ; Williams,
Waterman & Patterson, *Roofline* ; JEDEC JESD79-3 (DDR3) ; documentation Intel
« Stratix V Device Handbook » et « Quartus Prime » ; spécification OCP
*Microscaling Formats (MX) v1.0* ; PCI-SIG ; *DeepSeek-V4 Technical Report*.

