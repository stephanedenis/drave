# Rapport — le routage des experts était faux pour quatre gros modèles sur cinq

Session du 01/10 au 02/10, en autonomie. Question posée au départ : « pourquoi
V4-Flash ne se charge-t-il pas ? » La réponse s'est révélée plus large.

## 1. Ce qui a été trouvé

Le moteur routait **tous** les mélanges d'experts avec une seule convention,
choisie par un booléen : « softmax sur tous, top-k, renormalisation » — sauf
gpt-oss, « top-k sur les logits bruts, softmax sur les k ». Or les modèles de
cette machine en déclarent **quatre**, et deux d'entre eux ne se ramènent à
aucune des deux :

| modèle | arch | `expert_gating_func` | ce que le moteur faisait |
|---|---|---|---|
| Qwen3-30B-A3B | `qwen3moe` | absent → softmax | softmax ✓ |
| Qwen3-235B-A22B | `qwen3moe` | absent → softmax | softmax ✓ |
| gpt-oss-120b | `gpt-oss` | *(codé en dur)* | top-k brut + softmax, **biais compris** ✗ |
| Kimi-K2.7-Code | `deepseek2` | **2 — sigmoïde** | softmax ✗ |
| GLM-5.3 / -Flash | `glm-dsa`, `glm5next` | **2 — sigmoïde** | softmax ✗ |
| DeepSeek-V4-Flash | `deepseek4` | **4 — racine de softplus** | softmax ✗ |
| DeepSeek-V4.1-Flash | `deepseek41` | *(dans le JSON `config`)* | **dense : `n_expert = 0`** ✗ |

Et deux réglages n'étaient **lus nulle part** :

- `expert_weights_scale` (`routed_scaling_factor`) : **1,5** pour V4-Flash et
  V4.1, **2,5** pour GLM-5.3, **2,827** pour Kimi-K2.7. C'est un facteur
  d'échelle appliqué après la renormalisation : il change l'amplitude du flux
  résiduel, donc tout ce qui suit.
- `hash_layer_count` : les **trois premières couches** de V4-Flash ne routent
  pas par score mais par **table** (`ffn_gate_tid2eid.weight`, un tenseur I32 de
  `[129 280 × 6]` que le moteur ne lisait pas). L'expert est une fonction de
  l'identifiant du jeton.

Enfin, V4.1-Flash-Q2 ne déclare ses experts que sous les noms d'origine de
DeepSeek (`n_routed_experts`, `num_experts_per_tok`, `scoring_func`,
`routed_scaling_factor`, dans le JSON `<arch>.config` recopié par le
convertisseur). Le moteur ne lisait que les clefs normalisées : il prenait ce
modèle de 341 Go pour un modèle **dense**, et l'exécutait sans un seul expert.

## 2. Ce qui a été implémenté

Une seule fonction de routage (`router`, dans `drave-core/src/model.rs`),
appelée par le jeton seul **et** par le lot — les deux chemins avaient divergé
sur le biais de gpt-oss : le lot l'ajoutait aux poids, le jeton seul non. Une
porte verte sur un seul des deux ne disait rien de l'autre.

| convention | formule | modèles |
|---|---|---|
| `softmax` | softmax sur tous → top-k → renormalisation | Qwen3-MoE, défaut |
| `sigmoïde` | σ(logit) → top-k → renormalisation | Kimi-K2.7, GLM-5.3 |
| `softmax des poids` | top-k sur les logits **bruts + biais** → softmax sur les k | gpt-oss |
| `racine de softplus` | `√log(1+eˣ)` → top-k → renormalisation | V4-Flash, V4.1 |

puis `× expert_weights_scale`, et le routage par table quand
`ffn_gate_tid2eid.weight` existe. Quatre tests unitaires encodent les quatre
conventions avec des valeurs calculées à la main, plus un test qui vérifie que le
biais de gpt-oss ne départage que la **sélection** et n'entre pas dans les poids.

## 3. Ce qui est mesuré, et ce qui a bougé

| porte | avant | après | verdict |
|---|---|---|---|
| Qwen2.5-0.5B Q8_0 ctx 256 (dense) | 19,3885 | **19,3885** | inchangée, au bit près |
| Qwen3-30B clusters ctx 64, 8 jetons | 799,8557 | **799,8557** | inchangée, au bit près |
| gpt-oss-120b ctx 256 | 15,1757 | **15,6017** | **changée** — voir ci-dessous |

Le changement de gpt-oss est le seul effet visible sur les portes, et il est
justifié par le code de référence : `build_moe_ffn` de llama.cpp met le biais
dans `selection_probs` (la sélection) mais prend les poids dans `probs`
(`softmax(logits[choisis])`, **sans** biais). L'ancien code laissait le biais
dans le softmax. **15,1757 était auto-cohérent, pas juste.**

Au passage, une leçon de méthode : réunir les deux chemins de routage a d'abord
déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la
renormalisation était écrite `x / s` au lieu de `x * (1/s)`, ce qui n'est pas le
même flottant au dernier bit, et 48 couches l'amplifient. La comparaison
**ancien binaire / nouveau binaire sur le même modèle** (un `git worktree` sur
le commit précédent, 28 s de compilation) est ce qui l'a montré — pas la
relecture.

## 4. Ce que ce moteur ne sait toujours pas calculer

La vérification d'architecture ajoutée (`verifier_architecture`) refuse
maintenant les modèles non implémentés en nommant ce qui manque, au lieu de
mourir sur « tenseur `blk.3.attn_q.weight` absent » — une panne qui accuse le
fichier alors que c'est le moteur.

| modèle | poids | ce qui manque |
|---|---|---|
| Kimi-K2.7-Code | 1 026 G | MLA à rang faible, hyper-connexions |
| GLM-5.3 | 754 G | MLA à rang faible, hyper-connexions, attention par index |
| DeepSeek-V4.1-Flash | 755 G | les trois + engram + sortie à rang faible |
| DeepSeek-V4-Flash | 284 G | MLA à rang faible, hyper-connexions, sortie à rang faible |
| GLM-5.3-Flash | 321 G | identique à GLM-5.3 |

**Conséquence directe sur ce qui était publié** : aucun de ces cinq modèles n'a
jamais été exécuté par ce moteur. Les chiffres publiés à leur sujet — empreinte
mémoire, périodicité des experts, miroir, sonde engram — viennent d'analyses
**statiques** des tenseurs (inventaire, tailles, `mmap`), pas d'une passe avant.
C'est écrit dans le message de refus, et ça doit être écrit dans les rapports
concernés : un chiffre statique n'est pas invalidé, mais il ne dit rien du
calcul, et surtout rien du routage — qui, lui, était faux.

## 5. Ce qui reste ouvert

- La référence externe (llama.cpp) sur gpt-oss aux mêmes jetons est **lancée** ;
  elle doit confirmer ou contredire 15,6017. C'est la seule mesure qui tranche
  entre « le moteur a maintenant raison » et « le moteur a changé de bug ».
- Les conventions sigmoïde et racine-de-softplus sont implémentées et testées
  unitairement, mais **aucun modèle de cette machine ne peut les exercer**
  aujourd'hui (leurs architectures d'attention manquent). Elles ne sont donc pas
  validées de bout en bout — c'est une limite, pas un résultat.
- Le chemin `forward_mla` existe mais ne couvre que la MLA dense sans experts
  (modèle jouet `tools/mla_synthetique.py`). Le brancher sur le chemin principal,
  avec les experts et les hyper-connexions, est le prochain gros morceau.
