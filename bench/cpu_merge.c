/* Qtrinet — tri + dédoublonnage des contributions avant application
 *
 * Compilation : gcc -O3 -march=native -fopenmp -o cpu_merge cpu_merge.c && ./cpu_merge
 *
 * Résultats mesurés sur Hauru (50 M événements, 4096 destinations, 16 threads) :
 *
 *   (a) dispersion (1 écriture/événement)      3,36 G év/s   50 000 000 écritures
 *   (b) trié + replié (1 écriture/destination) 3,89 G év/s        4 111 écritures
 *   (c) tri radix 2 passes                     0,06 G év/s   = 838 ms
 *   rappel : ordre naturel (écarts décodés)    7,79 G év/s
 *
 * CONCLUSION : le tri + dédoublonnage divise les écritures par 12 000 mais ne
 * gagne que 16 % — les écritures n'étaient PAS le goulot. Le tri coûte 838 ms
 * là où l'accumulation en coûte 15 : il est ~50x plus cher que ce qu'il rapporte.
 *
 * L'ordre naturel (par source, listes de deltas) reste le meilleur : 7,79 G év/s.
 * Le dédoublonnage ne se justifie donc PAS pour la vitesse, seulement pour la
 * sémantique (fusion de contributions multi-plans ou multi-cartes).
 */
 *
 * (a) dispersion : un événement = une écriture aléatoire dans acc[]
 * (b) trié + replié : les contributions d'une même destination sont sommées
 *     dans un registre, puis écrites UNE fois → une écriture par destination
 * (c) coût du tri (radix 2 passes sur 16 bits)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <omp.h>

static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+1e-9*t.tv_nsec; }

#define NOUT 4096
#define NEV  (50u*1000u*1000u)
#define NPLANE 3                     /* multi-plans : 3 contributions par paire */

int main(void){
    uint32_t *dest = malloc((size_t)NEV*sizeof(uint32_t));
    float    *val  = malloc((size_t)NEV*sizeof(float));
    uint32_t rng=987654321u;
    for(size_t i=0;i<NEV;i++){ rng=rng*1103515245u+12345u; dest[i]=(rng>>8)%NOUT; val[i]=(rng>>16)&1?1.0f:-1.0f; }

    int th=16; omp_set_num_threads(th);

    /* ---------- (a) dispersion ---------- */
    {
        float *acc = calloc((size_t)th*NOUT,sizeof(float));
        double t0=now();
        #pragma omp parallel
        { int id=omp_get_thread_num(); float *my=acc+(size_t)id*NOUT;
          #pragma omp for schedule(static)
          for(long i=0;i<(long)NEV;i++) my[dest[i]] += val[i]; }
        double dt=now()-t0;
        printf("(a) dispersion (ecriture par evenement) : %6.2f G ev/s\n", NEV/dt/1e9);
        free(acc);
    }

    /* ---------- (c) tri radix 2 passes (8 bits) ---------- */
    uint32_t *tmp = malloc((size_t)NEV*sizeof(uint32_t));
    float    *tv  = malloc((size_t)NEV*sizeof(float));
    double t0=now();
    for(int pass=0; pass<2; pass++){
        size_t cnt[256]; memset(cnt,0,sizeof(cnt));
        int sh = pass*8;
        for(size_t i=0;i<NEV;i++) cnt[(dest[i]>>sh)&0xFF]++;
        size_t off[256], s=0;
        for(int b=0;b<256;b++){ off[b]=s; s+=cnt[b]; }
        for(size_t i=0;i<NEV;i++){ int b=(dest[i]>>sh)&0xFF; tmp[off[b]]=dest[i]; tv[off[b]]=val[i]; off[b]++; }
        memcpy(dest,tmp,(size_t)NEV*4); memcpy(val,tv,(size_t)NEV*4);
    }
    double dt_sort=now()-t0;
    printf("(c) tri radix 2 passes                    : %6.2f ms  (%5.2f G ev/s)\n",
           dt_sort*1e3, NEV/dt_sort/1e9);

    /* ---------- (b) parcours trie + repliement ---------- */
    {
        float *acc = calloc((size_t)th*NOUT,sizeof(float));
        long writes=0;
        double t0=now();
        #pragma omp parallel reduction(+:writes)
        {
            int id=omp_get_thread_num(); float *my=acc+(size_t)id*NOUT;
            long chunk=(long)NEV/th;
            long beg=(long)id*chunk, end=(id==th-1)?(long)NEV:beg+chunk;
            uint32_t cur=UINT32_MAX; float run=0;
            for(long i=beg;i<end;i++){
                if(dest[i]!=cur){ if(cur!=UINT32_MAX){ my[cur]+=run; writes++; } cur=dest[i]; run=0; }
                run+=val[i];
            }
            if(cur!=UINT32_MAX){ my[cur]+=run; writes++; }
        }
        double dt=now()-t0;
        printf("(b) trie + replie (1 ecriture/destination): %6.2f G ev/s   (%ld ecritures)\n",
               NEV/dt/1e9, writes);
        free(acc);
    }

    /* ---------- ordre naturel (par source) + repliement par plages ---------- */
    printf("\n--- rappel du noyau de decodage d'ecarts (ordre naturel par source) ---\n");
    printf("    7,79 G ev/s mesure precedemment\n");
    free(dest); free(val); free(tmp); free(tv);
    return 0;
}
