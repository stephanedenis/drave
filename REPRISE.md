# Reprise — état du projet et mode d'emploi pour une nouvelle session

> Rédigé à la fin d'une session longue. Tout ce qui suit est **mesuré**, pas
> déduit. Les valeurs de perplexité sont des **références de non-régression** :
> si une modification les change, c'est qu'elle a changé le calcul.

---

## 1. En une phrase

`qtrinet-core` est un moteur d'inférence Rust (~5 000 lignes, `std` seul) qui
charge les GGUF **en place** (aucune copie, aucune requantification), exécute les
projections soit en listes d'événements, soit en produit scalaire dense, gère les
MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
0,5 B au 120 B sur le CPU de cette machine.

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core && cargo build --release
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --chat --flux --prompt "Explique le ciel bleu en une phrase." \
    --n 64 --ctx 512 --threads 16 --temp 0
```

---

## 2. Références de non-régression

Corpus : `/tmp/wt2_txt.txt` = 20 000 premiers octets de `data/wikitext2_test.txt`.
**Régénérable** (à refaire si `/tmp` a été vidé) :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
head -c 20000 data/wikitext2_test.txt > /tmp/wt2_txt.txt
# les identifiants DOIVENT venir du tokenizer du modèle — jamais croisés
qtrinet-core/target/release/qtrinet-core models/Qwen2.5-0.5B-Q8_0.gguf \
    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_qwen.txt
qtrinet-core/target/release/qtrinet-core /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf \
    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss.txt
```

Le mode `--tokenize --fichier` **vérifie la réversibilité** (texte reconstruit
identique à la source) — les deux tokenizers la passent sur ce corpus.

| modèle | commande (abrégée) | perplexité attendue |
|---|---|---|
| Qwen2.5-0.5B Q8_0 | `--dense --limit 512` | **19,3885** |
| Qwen2.5-0.5B Q4_0 | `--q4 --limit 512` | **21,0110** |
| Qwen2.5-0.5B Q8_0, 6 bits | `--dense --bits-attn 6 --bits-ffn 6 --limit 512` | **19,3045** ← bat l'int8 |
| Qwen2.5-0.5B Q8_0, 4 bits | `--dense --q4 --limit 512` | **23,1323** |
| Qwen2.5-1.5B Q4_K_M | `--q4 --limit 256` | **12,9228** |
| Qwen2.5-VL-7B Q4_K_M | défaut, `--limit 128` | **10,9947** |
| Qwen3-30B-A3B MoE | `--dense --limit 128` | **7,6139** |
| gpt-oss-120b MXFP4 | `--dense --limit 64`, ids_oss | **20,8361** (63 jetons) |
| gpt-oss-120b MXFP4 | `--dense --limit 512`, ids_oss | **15,0757** (509 jetons, deux fenêtres) |
| gpt-oss-120b MXFP4 | `--dense --ctx 512 --limit 512`, ids_oss | **18,5803** (511 jetons, une fenêtre) |
| gpt-oss-120b MXFP4, YaRN | `QT_YARN=1`, `--ctx 512 --limit 512` | **174,3375** ← le YaRN statique du modèle |

> **gpt-oss : les anciens chiffres (39,8 puis 129,9) sont périmés.** Ils ont été
> mesurés avec deux bugs depuis corrigés : le biais `attn_output` ignoré et la
> fenêtre glissante appliquée aux 36 couches au lieu d'une sur deux. Le détail
> est dans `reports/rapport-gpt-oss-perplexite.md` ; la **référence externe**
> (llama.cpp, mêmes identifiants, sans BOS) donne 38,37 à 63 jetons et 169,67 à
> 511 en mode YaRN — notre moteur fait **mieux**, parce qu'il sait éteindre
> YaRN, qui coûte ici un facteur 9.

Toujours `--ctx 256 --abits 16 --threads 16`, et **jamais croiser les fichiers
d'identifiants** : nourrir un modèle avec le découpage d'un autre donne une
perplexité qui ne mesure que l'absurdité de l'entrée (42 127 mesuré ainsi).
Un garde-fou le détecte maintenant (identifiant ≥ vocabulaire = erreur franche).

---

## 3. Ce qui est implémenté et vérifié

| domaine | état |
|---|---|
| Formats lus **en place** | Q4_K, Q6_K, Q4_0, Q8_0, MXFP4, F16, F32 |
| MoE | routeur + biais de routeur, biais par expert, top-k, expert partagé, tranches contiguës |
| Architectures | q/k-norm (Qwen3), `post_attention_norm` (gpt-oss), sinks appris, fenêtre glissante, YaRN (défaut **off**), RoPE simple et partiel, `head_dim` déclaré |
| Tête de sortie | `output.weight` si non lié (bug corrigé), sinon `token_embd` |
| Tokenizers | Qwen2 **et** o200k (gpt-4o), tous deux lus du GGUF, sélectionnés par `tokenizer.ggml.pre` |
| Échantillonnage | température, top-k 40, top-p, **pénalité de répétition** (`--rep-penalty`, fenêtre `--hist`) |
| Génération | **sortie en flux** (`--flux`), **session multi-tours** (`--session`), arrêt sur fin de tour |
| Encodages | listes d'événements (push), dense int8 par ligne, dense 4 bits par bloc, **6 bits empaqueté par bloc** |
| GPU | noyaux PTX + API pilote, tête et projections opt-in (`QT_GPU=1`) |
| Outils | `--ppl`, `--plan` (placement), `--tokenize`, `--bits N` (simulation de précision) |
| Mesure | `--ppl-texte F` (identifiants du tokenizer du modèle), `--logits-bin F` (logits bruts), `--harmony*` (habillage harmony), `--swa-pattern N`, `--sans-fenetre` |
| Référence externe | `tools/ref_logits` (llama.cpp, mêmes identifiants, sans BOS) + `tools/compare_logits.py` |

**Vérifications externes déjà faites** (elles ont trouvé les bugs) : déquantification
Q4_K/Q6_K comparée à une référence F16 des mêmes poids ; tokenizer o200k comparé
à `/tokenize` ; perplexités recoupées avec `llama-perplexity` ; **logits comparés
un à un à llama.cpp** sur les mêmes identifiants (corrélation 0,999976 au premier
jeton, top-1 identique sur 63 positions, |ΔNLL| médian 0,076) ; tokenizer o200k
comparé à `llama-tokenize` sur 4 424 jetons (0 écart).

---

## 4. Pièges de l'environnement (tous rencontrés)

| piège | solution |
|---|---|
| **CUDA 13 : les symboles non versionnés du pilote échouent** (`cuMemAlloc` → erreur 201 alors que le contexte est courant) | utiliser partout les `_v2` |
| `nvcc` refuse gcc 15/16 (conflit d'en-têtes glibc) | compiler en **PTX avec clang**, le pilote compile à la volée |
| Python/numpy lent | `LD_PRELOAD=/usr/lib64/libopenblas.so.0` |
| 16 fils **battent** 32 sur ce moteur | ne pas sursouscrire la barrière tournante ; `--threads 16` |
| Épinglage NUMA | **perd** (23,2 → 25,5 s sur le 30 B) ; `--pin` déconseillé |
| Déport GPU | rentable seulement au-delà de **8 Mo** par matrice ; la tête n'est **pas** déportée (noyau non coalescé, 23 → 159 ms) |
| Charge de fond de la machine | fait varier les durées du simple au double : entrelacer les A/B, préférer les métriques déterministes |
| Les boucles d'analyse CLI sont **triplées** | un drapeau en **dernière** position était ignoré ; `--pin` et `--moe-topk` absents d'un des modes. Vérifier le mode visé |

---

## 5. Règles de méthode (chacune a coûté une erreur)

1. **Mesurer avant de conclure.** Le croisement push/pull était annoncé à 10 %,
   il est à 22 %. Dérouler un noyau « évident » n'a rien donné : le chemin était
   au mur mémoire, pas mal écrit.
2. **La double quantification est le piège le plus cher** : +12 % de perplexité
   sur Q4_0, et une simulation de précision qui annonçait 19,96 là où le format
   réel donne 19,30.
3. **Une hypothèse se teste, elle ne se défend pas.** Trois ont été réfutées cette
   session : cache KV pour l'attention (c'était la vectorisation), rotary partiel
   pour gpt-oss (185 → 1 095), YaRN (184,9 contre 39,8 sans).
4. **Vérifier quel chemin est actif** avant de déboguer un chiffre : la trace
   `[config]` au chargement dit quelles particularités ont été reconnues.
5. **Ne pas conclure sur 255 jetons** : l'écart peut être du bruit ; 510 minimum.
6. **Ne pas laisser un dépôt cassé** pour finir une refactorisation : revenir au
   dernier état valide est une option honorable.

---

## 6. Chantiers ouverts, par ordre de valeur

### a. gpt-oss : RÉSOLU (deux bugs corrigés), voir `reports/rapport-gpt-oss-perplexite.md`

Ce qui était annoncé « 39,8 au lieu de l'ordre de 6 » n'était pas un problème de
format ni de codage de position :

1. **`attn_output.bias` était ignoré** (gpt-oss a un biais sur Q, K, V **et O**) :
   39,80 → **20,84** à 63 jetons.
2. **La fenêtre glissante s'appliquait aux 36 couches** au lieu d'une sur deux
   (`layer_types` alterne, comme `set_swa_pattern(2)` de llama.cpp) : 129,9 →
   **15,08** à 511 jetons. Sans fenêtre du tout : 26,15 ; les deux extrêmes sont
   pires que le motif réel du modèle.
3. Un troisième bug latent (puits appris absents du softmax des couches pleines)
   est corrigé, **effet mesuré nul** sur gpt-oss (le chemin groupé les comptait).

**La prémisse « devrait valoir ~6 » était fausse** : llama.cpp, sur exactement
les mêmes identifiants et sans BOS, donne 38,37 (63 jetons) et 169,67 (511
jetons, YaRN) — notre moteur donne 41,11 et 174,34, avec une corrélation de
logits de 0,999976 et le même top-1 partout.

Deux faits à ne pas réapprendre :

- **YaRN ×32 (la configuration déclarée) coûte un facteur 9** : 174,34 contre
  18,58 à 511 jetons. Ce n'est pas un bug — HF, llama.cpp et l'implémentation
  officielle d'OpenAI appliquent le même YaRN statique (vérifié dans les
  sources). Notre défaut (YaRN éteint) est un choix **mesuré**.
- **Le format harmony rend le texte MOINS prévisible**, pas plus. Le modèle
  exige son canal `analysis` : après `<|start|>assistant<|channel|>`, p(analysis)
  = 0,9999 contre p(final) = 0,0001. Montages mesurés (même corpus) : 443
  (assistant consécutifs), 3 432 (consigne + texte), 8 463 (tours alternés),
  677 321 (suite réelle en `final` forcé), **26,0 pour le montage canonique**
  (système officiel + `analysis` puis `final`) contre **13,7 en brut pour le
  même texte**. L'hypothèse du §6.a.1 est donc **réfutée**.
- Effet de bord : `Gguf::open_meta` (en-tête seul) — `--tokenize` sur gpt-oss
  passe de ~60 s à **0,385 s** et chaque `--ppl` économise une lecture des 62 Go.

### b. YaRN « à retardement » (suite de a)

Appliquer l'étirement **seulement au-delà** de `initial_context_length` (4 096),
pour garder le gain à contexte court et l'extension longue. Protocole : corpus
de 8 000 jetons, `--ctx 4096`, quatre passes (simple/YaRN × court/long) ≈ 13 min
chacune sur le 120B. C'est la seule piste qui reste sur ce modèle.

### c. Refactoriser les boucles CLI (trois bugs de la même classe)

Une seule boucle pour les trois modes. La matière est prête : 50 drapeaux
dédupliqués, `struct Options` conçue, chaque mode destructurant ce dont il a
besoin. **À faire à froid**, avec un test après chaque groupe de drapeaux — une
substitution automatique a déjà corrompu les noms (`"--o.ids"`) et imposé un
retour en arrière. Cette session a encore trouvé un drapeau ignoré dans un mode
(`--attn-window` et `--attn-sinks` étaient analysés mais jamais appliqués en
inférence) : le symptôme est toujours le même.

### d. Noyaux GPU

Ils fonctionnent et donnent un résultat **identique au chiffre près** au CPU,
mais lisent une ligne par fil : les accès d'une même warp tombent dans des lignes
de cache différentes. Il faut une warp par ligne avec réduction, puis des noyaux
4 bits (Q4_K, Q6_K, MXFP4) — toute la famille Qwen est en Q4_K/Q6_K, donc
aujourd'hui rien de la leur n'est déportable.

### e. Échelles par bloc pour `DenseQ8`

Notre int8 quantifie avec une seule échelle **par ligne** ; le 6 bits, par bloc
de 32 — et il gagne. L'hypothèse à tester : le 6 bits ne gagne pas grâce à ses
deux bits, mais grâce à ses échelles plus fines. Si c'est vrai, l'int8 par bloc
repasserait devant à qualité égale. **C'est aussi l'écart résiduel avec
llama.cpp** (|ΔNLL| médian 0,076 sur gpt-oss) : nos activations sont quantifiées
sur 15 bits, une seule échelle par vecteur.

### f. Contexte long

Attention en O(contexte), KV en f32 non paginé : 800 Mo à 8 k pour le 30 B, et
+100 ms/jeton. Il faut KV quantifié et paginé, puis MLA pour les architectures
DeepSeek.

### g. Vision

Le chemin image du modèle VL n'existe pas.

---

## 7. Carte du dépôt

```
qtrinet-core/src/
  engine.rs     pool de fils, barrière, accumulateurs, noyau dense int8
  model.rs      chargement, forward, attention, MoE, génération, YaRN, sinks
  list.rs       encodages (PushMat, DenseQ4/6/8), noyaux AVX2, sources empruntées
  gguf.rs       lecteur GGUF, dequantification, vues en place
  tokenizer.rs  BPE byte-level, motifs qwen2 et gpt-4o
  gpu.rs        API pilote CUDA (sans crate), noyaux PTX
  main.rs       modes : inférence, perplexité, plan, tokenize
gpu/qtrinet_gpu.cu + .ptx    noyaux, compilés par clang
tools/ref_logits.cpp         référence llama.cpp : mêmes identifiants, sans BOS
tools/compare_logits.py      comparaison position par position (NLL, top-1, corrélation)
tools/harmony_canonique.py   montage harmony canonique (analysis puis final)
reports/rapport-travail-reel.md      ce que le moteur sait faire, tests réels
reports/rapport-gpt-oss-perplexite.md  les deux bugs de gpt-oss et la référence externe
docs/convertisseur.md                plan de chargement, résultats négatifs
reports/rapport-passage-a-l-echelle.md   modèle de coût, faisabilité par modèle
journal/                             sessions archivées automatiquement
```

Le journal s'archive à chaque commit (`tools/archive_sessions.py` +
`tools/session_report.py`, crochet git et crontab horaire).

---

## 8. Premier pas suggéré pour la nouvelle session

```bash
# 1. l'état est-il vert ? (Qwen ne doit pas bouger : les corrections de cette
#    session ne touchent que les modèles à biais de sortie et à fenêtre par couche)
cd qtrinet-core && cargo build --release && cargo test --release
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt \
    --ctx 256 --abits 16 --threads 16 --limit 512 --dense   # attendu 19,3885

# 2. si /tmp a été vidé, régénérer le corpus et les identifiants (§2)

# 3. gpt-oss : les deux chiffres de contrôle de cette session
./target/release/qtrinet-core /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf \
    --ppl /tmp/ids_oss.txt --ctx 256 --dense --threads 16 --limit 512   # attendu 15,08

# 4. puis §6.b : YaRN seulement au-delà de 4 096 (protocole dans le rapport)
```
