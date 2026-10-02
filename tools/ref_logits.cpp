// ref_logits.cpp — référence externe llama.cpp pour comparer les logits d'un moteur maison.
//
// Usage : ref_logits <modele.gguf> <ids.txt> <sortie.bin> [n_max]
//
//   - lit la liste d'identifiants (entiers séparés par des virgules et/ou des espaces)
//   - évalue la séquence EXACTE : positions 0..N-1, aucun BOS ajouté, une seule
//     séquence, un seul batch (n_ctx = N + marge, n_batch = n_ubatch = N)
//   - écrit <sortie.bin> en petit-boutiste :
//         int32 n_vocab
//         int32 n_pos
//         n_pos * n_vocab float32, ligne par position
//     la ligne i contient la distribution qui prédit ids[i+1] (donc n_pos = N-1)
//   - affiche n_pos, n_vocab, la NLL moyenne et la perplexité (log-softmax sur
//     les mêmes lignes, cible de la ligne i = ids[i+1])
//
// Compilation (voir ref_logits.md) :
//   g++ -O2 -std=c++17 tools/ref_logits.cpp -o tools/ref_logits \
//       -I /home/stephane/Data13TB/stephane/GitHub/llama.cpp/include \
//       -I /home/stephane/Data13TB/stephane/GitHub/llama.cpp/ggml/include \
//       -L /home/stephane/Data13TB/stephane/GitHub/llama.cpp/build/bin \
//       -lllama -lggml -lggml-base

#include "llama.h"

#include <cctype>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <regex>
#include <vector>
#include <fstream>
#include <string>
#include <thread>
#include <vector>

static bool lire_ids(const char * chemin, std::vector<llama_token> & ids) {
    std::ifstream f(chemin, std::ios::binary);
    if (!f) {
        std::fprintf(stderr, "ref_logits: impossible d'ouvrir %s\n", chemin);
        return false;
    }
    std::string texte((std::istreambuf_iterator<char>(f)), std::istreambuf_iterator<char>());
    const char * p = texte.c_str();
    const char * fin = p + texte.size();
    while (p < fin) {
        while (p < fin && !std::isdigit((unsigned char) *p) && *p != '-') {
            ++p;
        }
        if (p >= fin) {
            break;
        }
        char * stop = nullptr;
        long v = std::strtol(p, &stop, 10);
        if (stop == p) { // '-' isolé
            ++p;
            continue;
        }
        ids.push_back((llama_token) v);
        p = stop;
    }
    return true;
}

int main(int argc, char ** argv) {
    if (argc < 4) {
        std::fprintf(stderr, "usage: %s <modele.gguf> <ids.txt> <sortie.bin> [n_max] [--sans-yarn]\n", argv[0]);
        return 1;
    }
    const char * chemin_modele = argv[1];
    const char * chemin_ids    = argv[2];
    const char * chemin_sortie = argv[3];
    long n_max = 0; // 0 = tout le fichier
    if (argc >= 5 && argv[4][0] != '-') {
        n_max = std::strtol(argv[4], nullptr, 10);
        if (n_max < 0) {
            std::fprintf(stderr, "ref_logits: n_max invalide\n");
            return 1;
        }
    }

    std::vector<llama_token> ids;
    if (!lire_ids(chemin_ids, ids)) {
        return 1;
    }
    if (n_max > 0 && (long) ids.size() > n_max) {
        ids.resize((size_t) n_max);
    }
    const int32_t N = (int32_t) ids.size();
    if (N < 2) {
        std::fprintf(stderr, "ref_logits: il faut au moins 2 identifiants (recu %d)\n", N);
        return 1;
    }

    llama_backend_init();

    llama_model_params mparams = llama_model_default_params();
    mparams.n_gpu_layers = 0; // CPU uniquement

    llama_model * modele = llama_model_load_from_file(chemin_modele, mparams);
    if (modele == nullptr) {
        std::fprintf(stderr, "ref_logits: echec du chargement de %s\n", chemin_modele);
        return 1;
    }

    const int32_t n_vocab = llama_vocab_n_tokens(llama_model_get_vocab(modele));
    for (int32_t i = 0; i < N; ++i) {
        if (ids[i] < 0 || ids[i] >= n_vocab) {
            std::fprintf(stderr, "ref_logits: identifiant %d hors vocabulaire (n_vocab=%d) en position %d\n",
                         (int) ids[i], n_vocab, i);
            llama_model_free(modele);
            return 1;
        }
    }

    const size_t octets_logits = (size_t) N * (size_t) n_vocab * sizeof(float);
    if (octets_logits > (size_t) 2 << 30) {
        std::fprintf(stderr, "ref_logits: attention, %zu octets de logits (N=%d, n_vocab=%d)\n",
                     octets_logits, N, n_vocab);
    }

    llama_context_params cparams = llama_context_default_params();
    cparams.n_ctx         = (uint32_t) (N + 8); // marge
    // `--sans-yarn` (ou REF_SANS_YARN=1) : force le RoPE simple. gpt-oss déclare
    // YaRN ×32 ; comme qtrinet-core sait aussi tourner sans, il faut pouvoir
    // comparer les deux moteurs DANS LA MÊME configuration.
    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], "--sans-yarn") == 0) {
            cparams.rope_scaling_type = LLAMA_ROPE_SCALING_TYPE_NONE;
        }
    }
    if (std::getenv("REF_SANS_YARN") != nullptr) {
        cparams.rope_scaling_type = LLAMA_ROPE_SCALING_TYPE_NONE;
    }
    cparams.n_batch       = (uint32_t) N;
    cparams.n_ubatch      = (uint32_t) N;       // un seul batch physique
    cparams.n_outputs_max = (uint32_t) N;
    cparams.n_seq_max     = 1;
    cparams.embeddings    = false;
    cparams.flash_attn_type = LLAMA_FLASH_ATTN_TYPE_DISABLED;
    unsigned hw = std::thread::hardware_concurrency();
    int n_threads = (int) (hw == 0 ? 4 : (hw > 16 ? 16 : hw));
    cparams.n_threads       = n_threads;
    cparams.n_threads_batch = n_threads;

    // `--tensors REGEX` : imprime les premières valeurs des tenseurs dont le nom
    // correspond, PENDANT l'évaluation. C'est ce qui localise une divergence :
    // comparer les logits dit QU'il y a un écart, pas à quelle couche il naît.
    // Les noms sont ceux des `cb(...)` du graphe (« qr-0 », « kv_cmpr-0 »,
    // « k_pe-0 », « ffn_moe_out-3 »…).
    static const char * filtre_tensors = nullptr;
    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], "--tensors") == 0 && i + 1 < argc) { filtre_tensors = argv[i + 1]; }
    }
    if (const char * e = std::getenv("REF_TENSORS")) { filtre_tensors = e; }
    if (filtre_tensors != nullptr) {
        std::fprintf(stderr, "ref_logits: tenseurs filtrés par « %s »\n", filtre_tensors);
    }

    // Le filtre est capturé par la lambda : une variable statique de fichier
    // suffit, le programme est mono-modèle.
    if (filtre_tensors != nullptr) {
        cparams.cb_eval = [](ggml_tensor * t, bool ask, void * /*user*/) -> bool {
            const char * motif = filtre_tensors;
            if (t == nullptr || t->name == nullptr) { return false; }
            if (ask) {
                return std::regex_search(std::string(t->name), std::regex(motif));
            }
            std::fprintf(stderr, "[tensor] %s : type %d · ne = [%lld, %lld, %lld, %lld]\n",
                         t->name, (int) t->type,
                         (long long) t->ne[0], (long long) t->ne[1],
                         (long long) t->ne[2], (long long) t->ne[3]);
            // Jusqu'à 8 valeurs, en f32 quand c'est possible.
            if (t->type == GGML_TYPE_F32 || t->type == GGML_TYPE_F16) {
                std::vector<float> v(8, 0.0f);
                if (t->type == GGML_TYPE_F32) {
                    ggml_backend_tensor_get(t, v.data(), 0, 8 * sizeof(float));
                } else {
                    std::vector<ggml_fp16_t> h(8);
                    ggml_backend_tensor_get(t, h.data(), 0, 8 * sizeof(ggml_fp16_t));
                    for (int i = 0; i < 8; ++i) { v[i] = ggml_fp16_to_fp32(h[i]); }
                }
                std::fprintf(stderr, "          [0..8) =");
                for (int i = 0; i < 8; ++i) { std::fprintf(stderr, " %.6e", v[i]); }
                std::fprintf(stderr, "\n");
            }
            return true;
        };
    }
    llama_context * ctx = llama_init_from_model(modele, cparams);
    if (ctx == nullptr) {
        std::fprintf(stderr, "ref_logits: echec de la creation du contexte\n");
        llama_model_free(modele);
        return 1;
    }

    llama_batch batch = llama_batch_init(N, 0, 1);
    for (int32_t i = 0; i < N; ++i) {
        batch.token[i]    = ids[i];
        batch.pos[i]      = i;   // positions 0..N-1, aucun decalage BOS
        batch.n_seq_id[i] = 1;
        batch.seq_id[i][0] = 0;  // une seule sequence
        batch.logits[i]   = 1;   // logits pour toutes les positions
    }
    batch.n_tokens = N;

    const int32_t rc = llama_decode(ctx, batch);
    if (rc != 0) {
        std::fprintf(stderr, "ref_logits: llama_decode a retourne %d\n", rc);
        llama_batch_free(batch);
        llama_free(ctx);
        llama_model_free(modele);
        return 1;
    }

    const float * logits = llama_get_logits(ctx);
    if (logits == nullptr) {
        std::fprintf(stderr, "ref_logits: logits indisponibles\n");
        llama_batch_free(batch);
        llama_free(ctx);
        llama_model_free(modele);
        return 1;
    }

    const int32_t n_pos = N - 1; // la ligne i predit ids[i+1]

    std::FILE * out = std::fopen(chemin_sortie, "wb");
    if (out == nullptr) {
        std::fprintf(stderr, "ref_logits: impossible d'ecrire %s\n", chemin_sortie);
        llama_batch_free(batch);
        llama_free(ctx);
        llama_model_free(modele);
        return 1;
    }
    std::fwrite(&n_vocab, sizeof(int32_t), 1, out);
    std::fwrite(&n_pos,   sizeof(int32_t), 1, out);

    std::vector<float> ligne((size_t) n_vocab);
    double nll_cumul = 0.0;
    for (int32_t i = 0; i < n_pos; ++i) {
        const float * src = logits + (size_t) i * (size_t) n_vocab; // ligne de la position i

        double maxlogit = (double) src[0];
        for (int32_t v = 1; v < n_vocab; ++v) {
            if ((double) src[v] > maxlogit) {
                maxlogit = (double) src[v];
            }
        }
        double somme = 0.0;
        for (int32_t v = 0; v < n_vocab; ++v) {
            somme += std::exp((double) src[v] - maxlogit);
        }
        const double log_z = maxlogit + std::log(somme);
        nll_cumul += log_z - (double) src[ids[i + 1]];

        std::memcpy(ligne.data(), src, (size_t) n_vocab * sizeof(float));
        if (std::fwrite(ligne.data(), sizeof(float), (size_t) n_vocab, out) != (size_t) n_vocab) {
            std::fprintf(stderr, "ref_logits: ecriture incomplete a la position %d\n", i);
            std::fclose(out);
            llama_batch_free(batch);
            llama_free(ctx);
            llama_model_free(modele);
            return 1;
        }
    }
    std::fclose(out);

    const double nll_moyenne = nll_cumul / (double) n_pos;
    const double perplexite  = std::exp(nll_moyenne);

    std::printf("n_pos    = %d\n", n_pos);
    std::printf("n_vocab  = %d\n", n_vocab);
    std::printf("NLL moy  = %.6f\n", nll_moyenne);
    std::printf("perplexite = %.6f\n", perplexite);
    std::printf("fichier  = %s (%d x %d f32 + 8 octets d'en-tete)\n",
                chemin_sortie, n_pos, n_vocab);

    llama_batch_free(batch);
    llama_free(ctx);
    llama_model_free(modele);
    llama_backend_free();
    return 0;
}
