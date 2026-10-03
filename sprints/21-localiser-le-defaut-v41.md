# Sprint 21 — Localiser le défaut V4.1

- **Début** : 03:00 · **Fin** : 03:35 (35 min — l'investigation a avancé vite parce que
  chaque hypothèse avait son drapeau et sa mesure ; elle s'arrête ici, le défaut
  n'est pas trouvé mais il est cerné au chemin des experts, et le bloc suivant a
  son plan)
- **Objectif** : le bloc 20 a établi que **V4-Flash est juste** (PPL 1,875 sur huit
  répétitions, contre 1,844 pour llama.cpp) et que **V4.1 ne prédit pas** (3 677
  sans engram, 7 506 à 8 bits, top-1 0/31). Le défaut est dans un mécanisme propre
  à V4.1 : chaîne mHC retardée, compresseur des ratios 1 et 2, engram (partiellement
  innocenté). Le localiser, puis le corriger ou l'écrire.
- **Engagement de fin** : dépôt vert (tests + portes), machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. L'instrument de bisection, et huit hypothèses éliminées

Le test des répétitions (huit fois « The sky is blue. », ctx 64 ou 16) est
**fonctionnel** : V4-Flash y donne 1,875 (ctx 64) / 4,118 (ctx 16) et V4.1 y est à
3 677 (ctx 64) / 12 889 (ctx 16) — le hasard. Chaque ablation coûte 1 à 3 minutes,
et le résultat est sans ambiguïté :

| hypothèse | ablation | résultat | verdict |
|---|---|---|---|
| tokenizer | `tools/tokenize_llama` (llama.cpp) sur le même texte | identifiants **identiques** (`671,12709,344,8295,16,455,…`) | **éliminée** |
| chaîne mHC **retardée** | `DRAVE_V41_SANS_RETARD=1` (convention V4) | **41 544** contre 3 677 : dix fois PIRE | **éliminée** (le retard est la bonne règle) |
| **tête** (repliement final par la `pre`) | `DRAVE_V41_TETE_COPIE0=1` (copie 0) | 13 705 contre 12 889 | **éliminée** |
| **engram** | `DRAVE_SANS_ENGRAM=1` | 3 677 contre 4 799 : il nuit, mais le modèle est déjà cassé sans lui | **éliminée comme cause principale** |
| **blocs compressés** | `DRAVE_SANS_BLOCS=1` | **3 246 479** : 250 fois pire — les blocs portent l'essentiel du signal | **éliminée** |
| **compression** en entier | `DRAVE_SANS_COMPRESSION=1` (ratio 0 partout) | **1 948 572** : 150 fois pire | **éliminée** |
| **clamp SwiGLU** (`swiglu_limit` scalaire de V4.1, non lu) | lecture ajoutée | 12 889,408 → 12 889,418 : **aucun effet** (les portes ne dépassent pas 10 ici) | **éliminée** — mais la lecture est gardée : le fichier déclare ce clamp |
| **normes / explosion du résidu** | `DRAVE_DEBUG_ETAT=1` sur les deux modèles | V4.1 : 5 → 18 → 116 → 480 · V4-Flash : 9 → 10 → 97 → 421 — **même profil** | **éliminée** |
| le **chemin partagé** (attn_v4, compresseur, indexeur, hyper-connexions) | V4-Flash, mêmes conditions | **1,875 / 4,118** — il prédit | **éliminée** |
| enchaînement des trois ablations (ni compression, ni retard, ni engram) | les trois drapeaux ensemble | **2 521 650** : toujours le hasard | ⇒ le défaut est dans le chemin **partagé tel que V4.1 l'instancie** |

### 2. Ce que la mesure a établi, et qui restera

- Les **états portent l'information** : aux positions 2, 7 et 12 (le même contexte
  « … is »), les `l_last` ont des cosinus de 0,59 à 0,99 selon la couche — les
  états se ressemblent quand le contexte se ressemble. Le modèle n'est donc pas
  « débranché » : c'est la **prédiction** qui est au hasard.
- Les **blocs compressés sont la seule source de signal** : les retirer ou les
  désactiver rend le modèle 150 à 250 fois pire. Autrement dit, la **fenêtre
  brute** (les latents des 128 derniers jetons) ne sert à rien — ce qui, pour un
  modèle entraîné, est anormal (à ctx 16, elle couvre TOUT le contexte).
- Le **SwiGLU n'était pas borné** pour V4.1 (`swiglu_limit` scalaire ignoré) :
  défaut réel, corrigé, sans effet mesurable ici.

### 2bis. Deux vérifications de plus, et deux hypothèses de plus éliminées

- **L'embarquement est exact** : `l-hc_attn_pre-0-pos` (le vide de l'entrée de la
  couche 0) comparé aux lignes F16 de `token_embd.weight`, pour quatre positions →
  **écart 0,000e+00** · normes identiques. La porte d'entrée du modèle est juste.
- **Le biais de routeur** : V4.1 est le seul modèle du dépôt à en avoir DEUX
  (`exp_probs_b.bias` ≈ 9,83 et `exp_probs_b_vl.bias` ≈ 21,21 sur la couche 0 — des
  valeurs très différentes). Mesuré : avec le biais VL, la perplexité passe de
  12 889 à **535 688** (41× pire) → **le biais du texte est le bon**, et le
  routage est bien gouverné par le biais (ce qui est le principe du « noaux_tc » :
  le biais équilibre la charge, le contenu tranche à la marge). Le comportement du
  routeur est par ailleurs sain : 11 à 13 ensembles d'experts distincts sur 13
  jetons, aucun expert commun à tous.

### 2ter. Le routeur et la tête, vérifiés en numpy

- **La tête** : les logits du moteur pour six couples (position, jeton) ont été
  recalculés en numpy (`output.weight` Q8_0 déquantifié × `hidden_final` du vide) :
  écart **1e-4 à 1e-5 relatif** (le reste est l'arrondi du produit Q8_0) ✓.
- **Le routeur** : pour la couche 0, position 5, la sélection numpy
  (`hn = rmsnorm(hc_mel_ffn, ffn_norm)`, `logits = ffn_gate_inp · hn`,
  `scores = sqrt(softplus(logits))`, top-6 sur `scores + exp_probs_b`) rend
  **[0, 128, 155, 239, 269, 274]** — **exactement** la sélection de la trace du
  moteur ✓. Et les logits ont une dispersion saine (min −7,92, max 2,25, σ 1,14) :
  le biais, quoique grand (~9,8), est presque CONSTANT (étendue 0,29), donc c'est
  bien le contenu qui départage les experts ✓.

### 2quater. Un défaut SILENCIEUX trouvé en chemin : `--abits` au-delà de 16

En cherchant si la quantification d'activation était la cause, `--abits 24` a
donné **127 496** de perplexité contre 12 889 à 16 bits — *dix fois pire avec une
quantification plus fine*, ce qui n'a aucun sens. Cause : les activations
quantifiées circulent en `i16` (les noyaux d'experts prennent `&[i16]`) et les
conversions bornaient à ±32 767 — au-delà de 16 bits les valeurs étaient donc
SILENCIEUSEMENT ramenées à 32 767, soit une activation divisée par 2^(abits−16) —
et deux conversions n'étaient même pas bornées : elles **enroulaient** (modulo
65 536), ce qui donnait un résultat différent encore (116 415).

Corrigé : une seule fonction `niveaux_activation` borne à 16 bits, `poser_niveaux`
l'ANNONCE (« --abits 24 demandé : borné à 16 (32 767 niveaux), la borne du stockage
i16 »), les deux conversions non bornées le sont, et un test unitaire fixe la
borne (64 tests). Vérifié : `--abits 16` et `--abits 24` rendent maintenant
**exactement** 12 889,4182.

Ce n'est pas le défaut de V4.1 (16 bits est dans les bornes, et le résultat à
16 bits est inchangé), mais c'est un défaut bien réel : un drapeau qui changeait
le calcul d'un facteur 256 sans un mot.

### 3. La piste qui reste, et elle est étroite

Le défaut survit à tout ce qui est propre à V4.1 **sauf** ce qui touche à
l'instanciation de V4.1 dans le code partagé : les **noms et formes des tenseurs**
(les 24 noms de la couche 0 diffèrent de ceux de V4-Flash par deux biais de
routeur, et le diff ne montre AUCUN tenseur manquant), les **valeurs de
configuration** (ratios, o_groups, q_lora ✓), et la **règle du retard mHC** dont
la transcription vient de vLLM — la seule pièce non vérifiée contre une source
externe *exécutable*, et dont une variante (la convention V4) est dix fois pire
sans être bonne pour autant.

## 3bis. Le chemin des experts est VÉRIFIÉ (et ce n'est donc pas lui)

`tools/v41_experts_reference.py` recompose, depuis les tenseurs du fichier, tout
le chemin des experts routés : routeur (`ffn_gate_inp · hn` + `exp_probs_b`,
top-6, `scores/Σ × 1,5`), six experts déquantifiés en numpy (IQ2_XXS pour
`gate`/`up`, Q2_K pour `down`, recopiés de `formats.rs`/`gguf.rs` — donc l'accord
ne prouve pas le déquantificateur, validé à part contre libggml sur CE fichier),
l'activation (`silu(min(g,10)) · clamp(u,±10)`) et la somme pondérée ; puis compare
à `moe_down` :

| couche | position | experts choisis | écart max | relatif |
|---|---|---|---|---|
| 0 | 5 | [0, 128, 155, 239, 269, 274] | 3,381e-05 | **3,9e-05** |
| 0 | 12 | [61, 201, 202, 209, 319, 345] | 1,897e-05 | **5,2e-05** |

L'écart est celui d'une accumulation f32 contre f64 sur 2304 × 6 termes ; les
normes concordent à quatre décimales. **Le chemin des experts est donc juste** —
et il l'est même avec la quantification d'activation à 16 bits, puisque le numpy
emploie `hn` brut : la quantification à 16 bits est quasi sans perte ici ✓.

Conséquence : ni le MoE, ni la quantification, ni le routeur, ni l'embarquement,
ni la tête, ni le mHC (source publiée), ni le tokenizer, ni les formats ne sont en
cause. **Il ne reste que la composition de l'ATTENTION** — la seule pièce dont les
morceaux ont été vérifiés un par un, jamais l'ensemble.

## 3ter. L'attention : projections et normes vérifiées, un écart sur la rotation du Q

`tools/v41_attention_reference.py` recompose les premiers étages de l'attention
depuis les tenseurs (Q8_0 déquantifié en numpy) et les compare aux vides, ÉTAGE
PAR ÉTAGE — ce qui localise un désaccord tout seul. Couche 0, positions 5 et 12 :

| étage | écart relatif |
|---|---|
| `qr` = W_qa · norme(x) | **3,1e-06** ✓ |
| `qr_norm` | **1,2e-06** ✓ |
| `q_norm` (W_qb + norme par tête) | **6,9e-07** ✓ |
| `kv_rope` (W_kv + norme + rotation) | **6,9e-07** ✓ |
| `q_rope` | **3,6e+00** ✗ |

Deux enseignements :
1. **L'entrée de l'attention n'est pas `hc_attn_pre`** mais SA NORME
   (`rmsnorm(xin, attn_norm)`) — le premier essai donnait 0,53 d'écart sur `qr`
   pour cette seule raison. Le vide porte bien son nom, mais pas son étage.
2. Les projections et les normes de Q et de KV sont **justes** (1e-6), et la
   rotation du KV l'est aussi — donc la fonction de rotation est juste. Le seul
   écart est sur le Q **après** rotation, dans les 64 dernières composantes de
   chaque tête : les 448 premières sont identiques AU BIT PRÈS (écart exactement
   nul par tranche de 64), donc l'ordre des têtes et l'appariement des paires ne
   sont pas en cause.

Les deux tentatives d'inversion de l'angle appliqué (par paire, puis entre deux
positions) sont **non concluantes** : la première compare des angles modulo 2π
sans le dire, la seconde mélange la rotation et le changement d'entrée entre les
deux positions. Instrument à corriger avant de conclure : vider le `q` **juste
avant** la rotation (le `q_norm` existe déjà) et **juste après**, dans le même
gabarit que le KV, puis comparer les deux rotations sur les MÊMES valeurs.

## Portes

- `tools/portes.sh rapide` : **toutes vertes** après les changements du bloc —
  **64 tests**, Qwen 19,3885, clusters 799,8557, **V4-Flash 8430,4966** (la
  référence de non-régression, inchangée : la borne d'`--abits` et les conversions
  bornées ne touchent pas le chemin normal), engram, et les cinq modes du
  découpage.
- `tools/porte-flux.sh` : 5/5 (0,00e0 · 0,00e0 · 3,65e-2 · 0,00e0 · 4,45e-3).

## Rétrospective — garder / changer / doute

**Garder.**

- **Le test fonctionnel avant tout le reste** : « huit répétitions d'une phrase »
  coûte trois minutes et dit « ce modèle prédit ou non ». C'est lui qui a ouvert
  le bloc 20, et c'est lui qui a permis d'éliminer huit hypothèses en deux heures.
- **L'ablation par drapeau** : chaque hypothèse a son interrupteur
  (`DRAVE_V41_SANS_RETARD`, `DRAVE_V41_TETE_COPIE0`, `DRAVE_SANS_BLOCS`,
  `DRAVE_SANS_COMPRESSION`), et chacun ANNONCE ce qu'il fait. Le prochain
  défaut de ce genre se traquera de la même façon.
- **Le témoin systématique** : V4-Flash sur le même texte, dans le même moteur, à
  chaque étape. C'est lui qui a transformé « V4.1 est bizarre » en « V4.1 est
  cassé » puis en « le défaut est dans ce que V4.1 instancie ».

**Changer.**

- **Un test fonctionnel doit exister AVANT qu'un modèle soit déclaré exécutable.**
  Le dépôt a publié « V4.1 tourne » pendant des blocs sans jamais vérifier qu'il
  *prédit* — parce que toutes les vérifications étaient des égalités de composants
  (moteur contre SA transcription). La porte manquante est écrite ici : elle prend
  trois minutes, et elle aurait évité deux jours de chiffres non interprétables.
- **Un drapeau d'ablation qui ne rend pas le modèle MEILLEUR ne prouve rien.**
  Deux fois dans ce bloc, une ablation a empiré les choses (retard, blocs) : cela
  élimine l'hypothèse « c'est cette pièce qui est fausse » mais pas « cette pièce
  est fausse *autrement* ». Il faut les deux lectures.

**Doute.**

- Le défaut n'est pas trouvé, seulement cerné. Les suspects restants sont peu
  nombreux mais profonds : la règle du retard mHC (transcrite d'une source que je
  n'ai jamais exécutée) et deux ou trois valeurs de configuration.
- Le fichier V4.1 est un Q2 d'un modèle de 365 Go, avec des experts **IQ2_XXS ET
  Q2_K** : les deux déquantificateurs sont validés contre libggml
  (`tools/portes_formats.sh`), mais rien ne prouve que le fichier lui-même soit
  sain — et llama.cpp ne sait pas le charger, donc il n'existe aucune référence
  exécutable pour trancher.

### 2quinquies. Les vides qui manquaient pour vérifier les experts

Il n'existait aucun vide entre le routeur et la sortie de la couche : impossible de
comparer le chemin des experts à quoi que ce soit. Deux vides ajoutés :

- **`ffn_hn`** — l'entrée NORMÉE du MoE (`hc_mel_ffn` est AVANT la norme). Vérifié
  en numpy : `rmsnorm(hc_mel_ffn, ffn_norm, 1e-20)` donne le même vecteur à
  **1e-7 à 1e-6** (arrondi f32) sur deux couches et deux positions ✓ ;
- **`moe_down`** — la somme des experts ROUTÉS, avant l'expert partagé. C'est le
  vide qui rend le chemin des experts vérifiable : le routeur est déjà vérifié en
  numpy (sélection identique ✓), il ne reste qu'à recomposer
  `Σ_e w_e · W_d[e] · act(W_g[e]·hn, W_u[e]·hn)` avec les déquantificateurs IQ2_XXS
  et Q2_K — les deux sont validés contre libggml par `tools/portes_formats.sh`.

## Planning du bloc 22 — la composition, vérifiée contre numpy

Dix hypothèses sont éliminées et le défaut survit. Ce qui n'a JAMAIS été vérifié
pour V4.1, c'est la **composition** d'une couche : chaque pièce a été comparée à
une transcription, jamais l'ensemble. La suite, dans l'ordre :

1. **Le chemin des experts en numpy** : `moe_down` (vide neuf, bloc 21) contre
   `Σ_e w_e · W_d[e] · act(W_g[e]·hn, W_u[e]·hn)`, avec `hn` = `ffn_hn` (vérifié) et
   la sélection du routeur (vérifiée) — les déquantificateurs IQ2_XXS et Q2_K sont
   déjà validés contre libggml. C'est la dernière pièce jamais comparée pour V4.1.
2. **Puis l'attention en numpy** (couche 0, ratio 0) : `hc_attn_pre` → `q_rope`,
   `kv_rope`, `attn_brut`, `attn_out`, avec la rotation NORM et la sortie groupée
   `wo_a`/`wo_b`. C'est la seule vérification qui peut encore trouver
   une erreur de *composition* — celle que dix ablations ont manquée.
2. **Relire la règle du retard dans la source publiée** — FAIT au bloc 21 (vLLM
   `nvidia/model.py`, lignes 600-620 et 1015-1018) : notre chaîne et notre tête y
   sont conformes, mot pour mot. Ce point est donc clos.
3. **Les noms de tenseurs `hc_*`** — vérifiés : les 24 noms de la couche 0 de
   V4.1 et de V4-Flash sont identiques (deux biais de routeur en plus), aucun
   tenseur manquant.

## (Ancien) planning — la règle du retard, relue à la source

1. **Relire la règle mHC retardée dans la source publiée** (vLLM
   `deepseek_v4_1/nvidia/model.py`, et le portage `mudler/vllm.cpp` pour
   `deepseek_v41`) plutôt que dans notre transcription : c'est la seule pièce du
   chemin V4.1 qui n'a jamais été vérifiée contre une source *externe*. Points à
   contrôler un par un : quel `pre` replie l'attention, quel `pre` replie la FFN,
   ce que fait la tête, et si `post`/`comb` viennent du raccord courant ou du
   précédent.
2. **Vérifier les noms de tenseurs `hc_*`** pour V4.1 (les 24 noms de la couche 0
   ne les montrent pas tous) : un tenseur `hc_*` manquant serait chargé VIDE et le
   mélange serait faux **en silence**.
3. **Ablater le biais de routeur** (`exp_probs_b`) : V4.1 est le seul modèle du
   dépôt à en avoir deux (`exp_probs_b` et `exp_probs_b_vl`), et la question
   « biais dans la SÉLECTION ou dans les POIDS ? » a déjà coûté un défaut sur
   gpt-oss. Un drapeau d'ablation (sélection sans biais) trancherait en 3 minutes.
