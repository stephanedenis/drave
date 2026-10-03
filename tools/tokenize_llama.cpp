// Tokenise un texte avec le tokenizer d'un GGUF, via llama.cpp — référence
// EXTERNE pour la question « les identifiants que Drave fabrique sont-ils ceux
// du modèle ? ». Un décalage de tokenizer rendrait toute perplexité V4
// ininterprétable, et rien dans le dépôt ne le verrait : les identifiants sont
// dans le vocabulaire, donc acceptés.
//
// Compilation (la même que tools/ref_logits) :
//   LC=/home/stephane/Data13TB/stephane/GitHub/llama.cpp
//   g++ -O2 -std=c++17 tools/tokenize_llama.cpp -o tools/tokenize_llama \
//       -I $LC/include -I $LC/ggml/include -L $LC/build/bin -lllama -lggml -lggml-base
//
// Usage : LD_LIBRARY_PATH=$LC/build/bin ./tools/tokenize_llama <modele.gguf> "texte"
//         [--sans-bos]   (par défaut, n'ajoute AUCUN jeton spécial)
#include "llama.h"
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

int main(int argc, char ** argv) {
    if (argc < 3) { fprintf(stderr, "usage : %s <modele.gguf> \"texte\" [--sans-bos]\n", argv[0]); return 2; }
    const bool ajoute_bos = !(argc > 3 && strcmp(argv[3], "--sans-bos") == 0);
    llama_backend_init();
    auto mp = llama_model_default_params();
    mp.vocab_only = true;              // seul le vocabulaire nous intéresse
    llama_model * m = llama_load_model_from_file(argv[1], mp);
    if (!m) { fprintf(stderr, "chargement impossible\n"); return 1; }
    const llama_vocab * v = llama_model_get_vocab(m);
    const std::string texte = argv[2];
    std::vector<llama_token> ids(texte.size() + 8);
    int n = llama_tokenize(v, texte.data(), (int) texte.size(), ids.data(), (int) ids.size(),
                           ajoute_bos, /*special=*/true);
    if (n < 0) { fprintf(stderr, "tokenisation impossible (%d)\n", n); return 1; }
    ids.resize(n);
    for (int i = 0; i < n; ++i) printf("%d%s", ids[i], i + 1 == n ? "\n" : ",");
    llama_free_model(m);
    llama_backend_free();
    return 0;
}
