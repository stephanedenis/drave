# Les deux portes, phase par phase (P0 → P9)

> Écrit le 03/10 (bloc 27) pour répondre à une seule question, celle du mandat :
> **chaque phase a-t-elle ses deux portes, et où est la preuve ?** Chaque ligne
> renvoie à une mesure, pas à une intention. Ce qui n'est pas tenu est dit tenu
> pour ce qu'il est : impossible et nommé, ou sans effet et démontré.

Rappel des deux portes (`docs/plan-deepseek41-complet.md:142-149`) :

- **porte de correction** — comparaison à une référence **externe** (llama.cpp,
  ou une transcription numpy/vLLM indépendante) ;
- **porte Drave** — les flux : nombre d'événements/paires par jeton, trace écrite
  puis **rejouée à l'identique**, découpage en grappes, flux **lisible par un
  outil d'analyse**.

---

## Le tableau

| phase | porte de correction | porte Drave | état |
|---|---|---|---|
| **P0** — harnais, coût d'un jeton | `--config` annonce la bonne liste de manques (porte exécutée à chaque passage de `tools/portes.sh` : ✅) ; les deux côtés produisent les mêmes tenseurs nommés | un jeton sur V4-Flash affiche un nombre d'événements **non nul** avec sa provenance (attention · experts · partagé) | **FAIT** (02/10). Coût re-mesuré le 03/10 : **2,58 s/jeton** à ctx 512 (`proj+mlp` 1 414 ms, attention 1 138 ms) |
| **P1** — hyper-connexions | `hc_attn_pre` concorde à **1e-7** (arrondi f32), quatre positions (`reports/rapport-v4-couches-0-1.md`) | **TENUE le 03/10 (bloc 27)** — elle ne l'était pas : ni canal ni outil n'existaient, les 24 poids étaient **jetés**. Mesuré : Sinkhorn vérifié sur l'axe qu'il normalise en dernier (**1,14e-06**), 35 % des 16 connexions significatives, stabilité entre positions **0,92**, et **les 4 dominantes forment une permutation dans 43/43 couches** (`reports/rapport-hc-permutation.md`). Porte branchée : `tools/portes.sh` §7sexies | **FAIT + porte Drave fermée** |
| **P2** — épilogue d'attention | `attn_derope` corrélation **0,999996** avec llama.cpp ; `kqv_out`, `attn_out` | l'entrée de la sortie groupée est **la même liste** que celle qui sort de l'attention : c'est le contrat des modes de flux 1/2, exercé par `tools/porte-flux.sh` (modes exacts 0,00e0) | **FAIT** |
| **P3** — couches brutes | `l_last` corrélation **0,9998 – 0,99996** (llama.cpp, 4 positions) | `--trace-flux` sur deux couches puis `--flux-forcer` : perplexité identique — mesuré le 03/10 : **688 listes servies, 0 manquante**, écart **4,5e-06** (défini : ≤ 1e-5) | **FAIT** |
| **P4** — compresseur et HCA | première couche compressée : blocs + règle de visibilité vérifiés en numpy à **7,1e-07** | flux nouveau (blocs) **lisible** : lecteur DRVF v1/v2/v3, porte §7ter exécutée à chaque passage (51 lignes relues) | **FAIT** |
| **P5** — indexeur et CSA | `l_out-2` puis logits complets — c'est la porte de P6 (voir ci-dessous) | la liste de candidats est tracée ; **l'indexeur top-k n'est pas implémenté**, et c'est **démontré sans effet** tant que les blocs restent sous 512 (mesuré : 64 blocs à ctx 256, 128 à ctx 512) ; au-delà le moteur **refuse** au lieu de choisir faux | **FAIT**, limite nommée |
| **P6** — V4-Flash complet, listes, grappes | **TENUE**, trois fenêtres : 63 positions (min 0,9550 · moyenne 0,9852 · top-1 88,9 % · PPL +6,4 %), **255 positions** (99,6 % ≥ 0,95 · top-1 91,4 % · PPL +9,0 %), **511 positions** (99,6 % · top-1 93,0 % · PPL +4,3 %) — et l'accord **s'améliore avec la position** (0,98534 → 0,98934 → **0,99142**) | les 4 points : flux lisible (§7ter), rejeu défini et vérifié (§7quater), **découpage en grappes** (Qwen3-30B 799,8557 ; V4.1 découpé exact au bit près), paires/événements par jeton (profil à chaque passe) | **TENUE** |
| **P7** — V4.1 | **IMPOSSIBLE, et nommé** : llama.cpp refuse l'architecture (`unknown model architecture: 'deepseek41'`), il n'existe aucune référence exécutable. Ce qui est vérifiable sans elle l'est : douze vérifications de composants contre la source publiée (vLLM) et contre numpy — 1e-06 à 7e-07. Et le constat qui commande tout : **le modèle ne prédit pas** (top-1 **0/31**, NLL 11,657 nats pour un uniforme à 11,770) | découpage V4.1 **exact au bit près** (0,00e0 ; l'énigme de la `pre` reçue est fermée, `REPRISE.md` 02/10) ; engram : adressage dans les bornes, porte exécutée (479 723 rangées distinctes) | **composants faits ; modèle non prédictif ; conditions de sortie écrites** |
| **P8** — engram | vérifié contre la source publiée (`tools/engram_reference.py`, transcription 1:1) ; porte d'adressage à chaque passage | trace et outil d'analyse (`tools/analyse_engram.py`) ; vivacité mesurée par ablations (`DRAVE_SANS_ENGRAM`) | **FAITE et VIVANTE** |
| **P9** — noyaux natifs | `matvec_f32` parallèle par lignes : **×9,34** sur l'attention de V4.1, **bit à bit identique** (2 544 vides comparés, 0 écart) ; déquantification AVX2 Q2_K **bit-exacte contre libggml** (×1,33), IQ1_M (×1,07) | — (phase de noyaux, sans flux nouveau) | **mesure faite**. Ajout du 03/10 : produit scalaire vectorisé (`DRAVE_SIMD_DOT`), **×1,18 sur la passe et ×1,37 sur `proj+mlp`** mesurés en A/B entrelacé, écart de sortie **dit et mesuré** (+0,15 % de perplexité, corrélation 0,9981) — **opt-in**, le chemin par défaut reste bit à bit |

---

## Ce que ce tableau dit, et ce qu'il ne dit pas

**Ce qu'il dit.** Les deux portes sont tenues pour **P0 à P6** et **P8** ; pour
**P1**, la porte Drave manquait d'instrument et elle est fermée depuis ce bloc,
avec une mesure qui va plus loin que la porte (la structure est une
permutation). **P7** est le seul endroit où une porte est **impossible** — et
c'est écrit, avec sa condition de sortie (qu'un runtime sache charger
`deepseek41`, ou qu'on produise notre propre conversion et qu'on la compare).
**P9** est optionnel et son dernier ajout est une optimisation qui **dit** ce
qu'elle change, conformément au mandat.

**Une précision qui change la lecture des portes « de flux ».** Pour V4-Flash et
V4.1, le moteur **compte** les paires par jeton et par provenance (mesuré :
**16,2 G paires/jeton** — attention 6,2 G · experts 8,1 G · partagé 1,9 G), mais
la part **« en listes » est nulle** : le chemin V4 calcule **dense**, sur les poids
quantifiés empruntés au fichier (« dont en listes : 0,0 M — le reste est dense »,
profil de chaque passe). Autrement dit : *le flux est mesuré, et il est
transportable* (les cinq modes du découpage, exacts à 0,00e0 pour les modes 0, 1
et 3), *mais il n'est pas encore l'unité de calcul interne pour V4*. Les portes
Drave de P2 et P3 sont tenues au sens du **contrat d'échange** ; elles ne disent
pas que la couche calcule par listes. C'est l'écart entre « router des listes »
(la vision, axe 3) et « transporter des listes » (l'état actuel), et il mérite
d'être écrit noir sur blanc plutôt que découvert plus tard.

**Ce qu'il ne dit pas.** Deux réserves, nommées :

1. **Les fenêtres de la porte de correction restent froides au début.** Le
   diagnostic par tranches montre que l'accord ne se dégrade pas avec la
   position, mais les premiers jetons sont notés sans contexte — c'est la nature
   du protocole, pas un défaut caché.
2. **La porte Drave de P6 n'est tenue « à chaque passage » que sur le petit
   modèle.** Le rejeu sur V4-Flash (688 listes, 4,5e-06) est mesuré **à la
   demande**, pas dans `portes.sh` — une passe V4 coûte des minutes. L'écart
   entre ce que la porte *dit* et ce qu'elle *vérifie à chaque passage* est écrit
   ici plutôt que masqué.

**Ce qui a changé le 03/10** (blocs 23 à 27) et qui a rendu ce tableau
nécessaire : la porte de correction a des **critères mesurés** et un **outil qui
rend un verdict** (`tools/compare_logits.py --porte`, branché §7quinquies) ; elle
est passée de 4 à **511 positions** ; le rejeu a une **définition** (0 liste
manquante, écart ≤ 1e-5) ; la porte Drave de P1 est **fermée** ; et deux chiffres
publiés ont été **corrigés** parce qu'une mesure les a contredits (le gain du
SIMD, et le « coût qui croît avec la position » qui était le disque dur).
