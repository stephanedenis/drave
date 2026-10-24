# 2. Modèles et architectures

> **Famille 2 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

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

**Jeton (token)** — Le découpage **technique** du modèle : un mot court, un fragment de mot ou un signe. Le moteur
raisonne en jetons, jamais en caractères (`docs/format-flux.md:29`). **Où** : `--tokenize`, `src/tokenizer.rs`.
**Vocabulaire** : voir § 1 (« Jeton », « Représentation sémantique neutre ») — le jeton ne désigne **jamais** la
RSN.

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

