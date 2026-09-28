# ref_logits — référence externe llama.cpp pour comparer les logits

Outil autonome (un seul fichier C++) qui évalue une séquence d'identifiants **exacte**
avec llama.cpp et exporte les distributions de logits en binaire, plus la perplexité.
Sert de référence pour valider les logits de `qtrinet-core`.

## Compilation (commande exacte qui marche)

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
LC=/home/stephane/Data13TB/stephane/GitHub/llama.cpp
g++ -O2 -std=c++17 tools/ref_logits.cpp -o tools/ref_logits \
    -I $LC/include -I $LC/ggml/include \
    -L $LC/build/bin -lllama -lggml -lggml-base
```

Aucune option supplémentaire n'est nécessaire (pas de `-fopenmp`, pas de `-lggml-cpu` :
le backend CPU est chargé dynamiquement par `libggml`). Version de llama.cpp utilisée :
`libllama.so.0.0.11001` (commit `a8f2635f`).

## Utilisation

```bash
LD_LIBRARY_PATH=/home/stephane/Data13TB/stephane/GitHub/llama.cpp/build/bin \
  ./tools/ref_logits <modele.gguf> <ids.txt> <sortie.bin> [n_max]
```

- `ids.txt` : entiers séparés par des virgules et/ou des espaces (les `n_max` premiers).
- Évaluation : positions `0..N-1`, **aucun BOS ajouté**, une seule séquence,
  un seul batch (`n_ctx = N + 8`, `n_batch = n_ubatch = N`, Flash-Attention désactivé, CPU).
- Sortie standard : `n_pos`, `n_vocab`, NLL moyenne, perplexité.

## Commande de validation

```bash
LD_LIBRARY_PATH=/home/stephane/Data13TB/stephane/GitHub/llama.cpp/build/bin \
  ./tools/ref_logits models/Qwen2.5-0.5B-Q8_0.gguf /tmp/ids_qwen.txt \
  /tmp/ref_logits_qwen05_q8_64.bin 64
```

## Nombres obtenus (Qwen2.5-0.5B-Q8_0, 64 premiers ids de /tmp/ids_qwen.txt)

| Mesure | Valeur |
|---|---|
| `n_pos` | 63 |
| `n_vocab` | 151936 |
| NLL moyenne | 3.316958 |
| **Perplexité** | **27.576** (Q4_0 : 28.850) |
| Taille du fichier | 38 287 880 octets = 8 + 63 × 151936 × 4 |
| Mémoire de pointe | 629 Mio (RSS), durée 0,7 s |

Contrôles de cohérence effectués :

- perplexité calculée de deux façons indépendantes (log-softmax interne C++ et relecture
  du binaire en Python) : identiques à 1e-5 ;
- somme des probabilités d'une ligne = 1,000000 ; exactitude argmax = 26/63 (41 %) ;
- déterminisme : deux exécutions donnent des binaires au MD5 identique ;
- **cohérence causale** : un run avec `n_max=32` reproduit *bit à bit* les 31 premières
  lignes du run à 64 → positions et absence de BOS correctes ;
- la perplexité de 27,58 est portée par l'amorce froide de la fenêtre : les positions
  0..4 ont une NLL de 5,4 / 11,8 / 5,4 / 5,1 / 3,7 (le fichier commence par un simple
  jeton `\n`), tandis que les positions ≥ 5 donnent une perplexité de **21,3** — dans la
  plage attendue (15–25). Un moteur câblé de travers donnerait 1,0 ou 10^5.

## Format du fichier binaire (petit-boutiste)

```
offset 0   : int32  n_vocab
offset 4   : int32  n_pos
offset 8   : n_pos × n_vocab × float32
```

Les lignes sont dans l'ordre des positions : la ligne `i` (0-indexée) contient la
distribution qui prédit le jeton d'indice `i+1` (cible = `ids[i+1]`). Avec `N` jetons
évalués, `n_pos = N - 1` (la dernière position n'a pas de cible) ; la ligne `i` commence
à l'octet `8 + i * n_vocab * 4`.

## Limites

- Le dernier jeton n'a pas de distribution exportée (`n_pos = N - 1`).
- `n_batch = n_ubatch = N` : au-delà de quelques milliers de jetons, la mémoire des
  logits de llama.cpp croît en `N × n_vocab × 4` (un avertissement est émis au-delà de
  2 Gio) ; utiliser `n_max` pour borner.
