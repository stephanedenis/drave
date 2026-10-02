// Imprime les tables de ggml au format Rust — celles que le moteur embarque
// pour déquantifier IQ2_XXS, IQ1_M, IQ1_S et IQ3_XXS.
//
// Une seule valeur recopiée à la main qui se trompe ruine des dizaines de Go de
// poids, et l'erreur est SILENCIEUSE si la table reste plausible (une grille
// légèrement fausse donne des poids légèrement faux). D'où l'extraction par
// programme, et la comparaison automatique de `extraire_tables_ggml.sh verifier`.
#define GGML_COMMON_IMPL_C
#include <stdio.h>
#include <stdint.h>
#include "ggml.h"
#include "ggml-common.h"

int main(void) {
    printf("// Table extraite de ggml-common.h par tools/extraire_tables_ggml.sh.\n");
    printf("pub static IQ2XXS_GRID: [[u8; 8]; 256] = [\n");
    for (int i = 0; i < 256; i++) {
        printf("    [");
        // Grille lue OCTET PAR OCTET par le noyau IQ2_XXS : l'ordre des octets
        // d'un petit-boutiste est la donnée elle-même.
        for (int j = 0; j < 8; j++) printf("%u,", (unsigned)((iq2xxs_grid[i] >> (8*j)) & 0xFF));
        printf("],\n");
    }
    printf("];\n\n");

    printf("pub static KSIGNS_IQ2XS: [u8; 128] = [\n    ");
    for (int i = 0; i < 128; i++) {
        printf("%u,", ksigns_iq2xs[i]);
        if (i % 16 == 15) printf("\n    ");
    }
    printf("\n];\n\n");

    printf("pub static IQ1S_GRID: [[i8; 8]; 2048] = [\n");
    for (int i = 0; i < NGRID_IQ1S; i++) {
        uint64_t v = iq1s_grid[i];
        printf("    [");
        for (int j = 0; j < 8; j++) printf("%d,", (int)(int8_t)((v >> (8*j)) & 0xFF));
        printf("],\n");
    }
    printf("];\n\n");

    printf("pub static KVALS_IQ4NL: [i8; 16] = [\n    ");
    for (int i = 0; i < 16; i++) printf("%d,", (int)kvalues_iq4nl[i]);
    printf("\n];\n\n");

    printf("pub static IQ3XXS_GRID: [[u8; 4]; 256] = [\n");
    for (int i = 0; i < 256; i++) {
        printf("    [");
        // `iq3xxs_grid` est un tableau d'uint32_t lu OCTET PAR OCTET par le
        // noyau (`(const uint8_t *)iq3xxs_grid + code`) : l'ordre des octets
        // d'un petit-boutiste est donc la donnée elle-même.
        for (int j = 0; j < 4; j++) printf("%u,", (iq3xxs_grid[i] >> (8*j)) & 0xFF);
        printf("],\n");
    }
    printf("];\n");
    return 0;
}
