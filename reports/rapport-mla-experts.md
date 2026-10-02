# Rapport — MLA à rang faible et formats sans noyau : GLM-5.3 et Kimi deviennent calculables

Session du 02/10, en autonomie, suite du [rapport sur le
routage](rapport-routage-experts.md). Le point de départ était un refus : le
moteur ne savait pas calculer DeepSeek-V4-Flash. Le trajet, lui, a traversé
quatre verrous qui accusaient tous le fichier alors que c'était le moteur.

## 1. Les quatre verrous, dans l'ordre où ils sont tombés

| ce qui échouait | ce que le moteur disait | ce qui manquait vraiment |
|---|---|---|
| V4-Flash, V4.1 | `tenseur blk.3.attn_q.weight absent` | attention MLA à rang faible |
| GLM-5.3, Kimi | `mélanges d'experts chargés : 0/79` | formats d'experts IQ sans noyau |
| GLM-5.3 | `projection sans aucun format` | FFN dense des 3 premières couches |
| V4, GLM-Flash | *(rien : ça tournait)* | hyper-connexions, index, sortie à rang faible |

Aucun de ces messages ne nommait la cause. Un GGUF de 216 Go ne perd pas ses
tenseurs : c'est le moteur qui ne les lisait pas.

## 2. Attention MLA (`attn_mla`)

Le moteur n'avait que Q/K/V denses. La MLA remplace les trois par **quatre
projections de rang faible** et un cache **latent** :

- `Q = W_q_b · norm(W_q_a · h)` — la norme entre les deux est essentielle, et
  l'oublier donne des scores faux d'un facteur qui dépend de la norme de l'état ;
- `c_kv = norm(W_kv_a · h)`, `k_rope = RoPE(W_kv_a · h)` — seules ces
  `kv_lora + qk_rope` valeurs sont stockées par position ;
- `k_nope` et `v` sont **reconstruits à la lecture** par `W_k_b` et `W_v_b`.

Pour GLM-5.3 : 576 valeurs par jeton au lieu de 448 par tête dense (28 672 pour
64 têtes). C'est tout l'intérêt de MLA, et c'est aussi ce qui rend le cache
indépendant du nombre de têtes.

Deux dispositions de la remontée KV coexistent, et elles ne se devinent pas au
nom de l'architecture :

| disposition | tenseurs | qui |
|---|---|---|
| combinée | `attn_kv_b` `[kv_lora, nh·(qk_nope+v)]` | harnais `tools/mla_synthetique.py` |
| séparée | `attn_k_b` `[nh, kv_lora, qk_nope]`, `attn_v_b` `[nh, kv_lora, v]` | Kimi-K2.7, GLM-5.3, DeepSeek-V4 |

Le choix se fait sur la **présence** des tenseurs. Dans la disposition séparée,
l'index de sortie est le plus lent (`k_nope[o] = Σ_c k_b[hh][c][o]·c_kv[c]`) :
l'écrire dans l'autre sens donne des scores plausibles et faux.

**Ce qui n'a PAS été dupliqué** : le reste de la couche — résidu, FFN dense *ou*
mélange d'experts, tête de sortie — est partagé avec le chemin dense. Une
seconde copie du bloc MoE aurait été la troisième divergence de ce dépôt. Le
seul chemin qui reste séparé est le **lot** : les modèles MLA repassent par le
jeton seul, parce que le chemin par lots ne connaît que Q/K/V denses.

## 3. Formats de super-bloc sans noyau

`source_de` ne connaissait que Q4_K, Q6_K, MXFP4 et Q4_0. Les autres formats
n'avaient **pas de noyau** : le chargeur refusait donc la couche. GLM-5.3 en
mélange quatre sur cinq couches :

| couche | `ffn_down_exps` | `ffn_gate_exps` |
|---|---|---|
| 53 couches | IQ3_XXS | IQ1_S |
| 22 couches | IQ3_XXS | IQ2_XXS |
| 4 couches | **IQ4_XS** | IQ1_S |
| 1 couche | **Q3_K** | IQ2_XXS |

D'où « 71/79 » : les 5 couches fautives étaient exactement celles qui
introduisaient IQ4_XS et Q3_K, et rien ne le disait.

La voie ajoutée (`Source::Dequant`) **déquantifie le super-bloc de 256 poids
puis accumule en f32**. Elle est juste par construction — les huit
déquantificateurs concernés sont comparés à libggml au bit près
(`tools/portes_formats.sh`) — et parallélisée par lignes de sortie. Elle ne
coûte que le temps de la déquantification. Un test vérifie que `sans_noyau` et
`dequant_grille` couvrent le même ensemble : une divergence ferait refuser une
couche pour un format lisible, ce qui est exactement l'histoire des « 0/79 ».

## 4. Deux bugs trouvés en chemin, tous deux dans du code déjà publié

- **FFN dense vidée pour tout le modèle.** `wgate: if cfg.n_expert > 0 {
  Proj::vide() }` supposait qu'un modèle à experts n'a *que* des couches à
  experts. Faux pour GLM-5.3 (3 couches denses puis 76) et pour Kimi (1 puis
  60). La décision se prend maintenant **couche par couche**, sur la présence
  effective du mélange.
- **Un garde-fou a cassé une porte verte.** Le contrôle « le modèle déclare des
  experts mais aucun tenseur d'experts n'est lisible » refusait le modèle en
  clusters de la porte publiée (`qwen3-30b-8clusters-v2`), où les experts sont
  préfixés `cl0/…`. Détecté tout de suite parce que la porte existait ; le
  contrôle ne s'applique plus quand un mapping est actif.

## 5. Ce qui est mesuré

- **GLM-5.3 (216 Go)** : 79 couches MLA, 76/79 mélanges d'experts chargés (les
  3 autres sont denses, c'est le modèle), ~85 Go de RSS au chargement, dont
  ~52 Go de tenseurs MLA déquantifiés en f32 — un coût réel, pas un détail :
  ces huit tenseurs par couche ne sont pas empruntés au fichier.
- **Kimi-K2.7 (1 026 G poids)** : `--config` annonce « calculable : oui »,
  61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton.
- **Portes inchangées au bit près** après le remplacement de `matvec_q4` par un
  aiguillage : Qwen2.5-0.5B **19,3885**, Qwen3-30B en clusters **799,8557**.
- **48 tests** (46 avant, +2 sur la cohérence des tables de formats).

## 6. GLM-5.3 tourne — et le chiffre n'est pas encore croyable

| mesure | valeur |
|---|---|
| chargement | 379 à 553 s (216 Go, dont ~52 Go de MLA déquantifiée en f32) |
| mémoire de pointe | ~90 Go de RSS |
| couches | 79 MLA, 76/79 avec mélange d'experts chargé (les 3 autres sont denses) |
| débit, première mesure | **253 s par jeton** |
| débit, après suppression des allocations par bloc | **53 s par jeton** (dont 20 s d'attention) |
| perplexité sur 3 jetons | **7 300 931** — inexploitable |

Deux choses, et il faut les séparer :

1. **La mécanique fonctionne** : les 79 couches s'enchaînent, les experts IQ sont
   déquantifiés, la MLA tient son cache latent, rien ne panique. C'est la
   première fois que ce modèle calcule quoi que ce soit ici.
2. **Le résultat est faux ou non validé** — et une perplexité de 7 millions n'est
   pas « un peu faux » : le modèle est *sûr de lui et à côté*. Les causes
   possibles sont listées ci-dessous ; tant qu'aucune n'est écartée par une
   mesure, ce chiffre ne doit pas être publié comme un résultat.

Ce qui a déjà été écarté par lecture du code de référence : les dimensions
(`qk_nope = 192`, `qk_rope = 64`, `v = 256`, `kv_lora = 512` — toutes cohérentes
avec `attention.key_length_mla` et les formes des tenseurs), le type de rotation
(`LLAMA_ROPE_TYPE_NORM`, appariement `i` / `i + n_rot/2`), la base de rotation
(`rope.freq_base = 8e6`, lue), et l'indexeur DSA (il ne sert qu'au-delà de
`index_topk = 2048`, et un contexte de 16 jetons garde toutes les clés — donc
l'omettre est exact, pas approché).

Corrigé au passage, et c'était un vrai bug : **l'expert partagé n'était jamais
calculé**. `vue_unique` exigeait trois dimensions ; les tenseurs
`ffn_*_shexp.weight` sont en 2D (`[n_ff, hidden]`), donc `shexp` restait `None`
et un FFN entier, toujours actif, manquait à chaque couche de chaque modèle
DeepSeek/GLM/Kimi. C'est le genre d'omission qui ne se voit pas à la lecture et
qui ne se pardonne pas au calcul.

## 7. Ce qui reste ouvert, et qui est le plus important

1. **Aucune validation externe de la MLA.** Elle est implémentée d'après le C de
   llama.cpp, testée par ses portes internes, mais elle n'a pas encore été
   comparée à une référence sur les mêmes jetons. Tant que ce n'est pas fait,
   « GLM-5.3 tourne » ne veut pas dire « GLM-5.3 est juste » — et vu l'histoire
   de cette session, la distinction vaut.
2. **Pas de noyau IQ.** Le débit des gros modèles est celui de la
   déquantification, pas celui du produit. C'est un choix assumé
   (exactitude d'abord) mais il plafonne Kimi et V4.
3. **Hyper-connexions, attention par index, sortie à rang faible** : non
   implémentées. Elles bloquent GLM-5.3-Flash, V4-Flash et V4.1. `--config` le
   dit en 50 ms sans charger le modèle.
4. Le chemin MLA n'a ni fenêtre glissante ni YaRN : à contexte long, les
   modèles concernés demanderont l'un ou l'autre.
