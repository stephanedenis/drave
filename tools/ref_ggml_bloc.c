// Référence ggml pour un super-bloc : imprime les 256 poids que **libggml**
// produit pour le bloc demandé.
//
//   ref_ggml_bloc <fichier.gguf> <offset octets> <type ggml>
//
// Pourquoi ce programme existe : nos déquantificateurs (Q2_K, Q5_K, IQ2_XXS,
// IQ1_M) ont chacun été écrits à partir du C de ggml, et chacun s'est trompé au
// premier essai — mauvais pas d'indexation des bits hauts (IQ2_XXS), mauvais
// ordre des champs (IQ1_M : les échelles sont en DERNIER), mauvais indice
// d'échelle (Q2_K). Comparer à une réimplémentation en Python ne prouve rien :
// elle partage la même lecture du format. Ici la référence est la bibliothèque
// elle-même, liée telle quelle.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ggml.h"
#include "ggml-common.h"
#include "ggml-quants.h"

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: ref_ggml_bloc <fichier> <offset> <type>\n"); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("fopen"); return 1; }
    if (fseek(f, atol(argv[2]), SEEK_SET) != 0) { perror("fseek"); return 1; }
    const int type = atoi(argv[3]);
    // 256 octets suffisent à tous les blocs de 256 poids ; les types à bloc de
    // 32 (Q4_0, Q8_0, MXFP4…) sont lus 8 fois de suite.
    float y[256];
    const int nb = 256;
    switch (type) {
        // F32, F16 et BF16 ne sont pas des types « quantifiés » : ggml n'a pas
        // de dequantize_row_* pour eux, la conversion est la lecture elle-même.
        case 0:  { float b[256];  if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   memcpy(y, b, sizeof(b)); break; }
        case 1:  { ggml_fp16_t b[256]; if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   for (int i = 0; i < nb; i++) y[i] = ggml_fp16_to_fp32(b[i]); break; }
        case 2:  { block_q4_0 b[8];  if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q4_0(b, y, nb); break; }
        case 3:  { block_q4_1 b[8];  if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q4_1(b, y, nb); break; }
        case 6:  { block_q5_0 b[8];  if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q5_0(b, y, nb); break; }
        case 7:  { block_q5_1 b[8];  if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q5_1(b, y, nb); break; }
        case 8:  { block_q8_0 b[8];  if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q8_0(b, y, nb); break; }
        case 10: { block_q2_K b;     if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q2_K(&b, y, nb); break; }
        case 11: { block_q3_K b;     if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q3_K(&b, y, nb); break; }
        case 12: { block_q4_K b;     if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q4_K(&b, y, nb); break; }
        case 13: { block_q5_K b;     if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q5_K(&b, y, nb); break; }
        case 14: { block_q6_K b;     if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_q6_K(&b, y, nb); break; }
        case 16: { block_iq2_xxs b;  if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_iq2_xxs(&b, y, nb); break; }
        case 18: { block_iq3_xxs b;  if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_iq3_xxs(&b, y, nb); break; }
        case 19: { block_iq1_s b;    if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_iq1_s(&b, y, nb); break; }
        case 23: { block_iq4_xs b;    if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_iq4_xs(&b, y, nb); break; }
        case 29: { block_iq1_m b;    if (fread(&b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_iq1_m(&b, y, nb); break; }
        case 30: { ggml_bf16_t b[256]; if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   for (int i = 0; i < nb; i++) y[i] = ggml_bf16_to_fp32(b[i]);
                   break; }
        case 39: { block_mxfp4 b[8]; if (fread(b, sizeof(b), 1, f) != 1) return 1;
                   dequantize_row_mxfp4(b, y, nb); break; }
        default:
            fprintf(stderr, "type %d non géré par la référence\n", type);
            return 2;
    }
    for (int i = 0; i < 256; i++) printf("%.7f\n", y[i]);
    return 0;
}
