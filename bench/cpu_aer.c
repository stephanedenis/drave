/* Qtrinet — mesure des limites réelles du CPU pour l'architecture push (AER)
 *
 * Compilation :  gcc -O3 -march=native -fopenmp -o cpu_aer cpu_aer.c && ./cpu_aer
 *
 * Résultats mesurés sur Hauru (2x Xeon E5-2687W v3, openSUSE Tumbleweed) :
 *
 *   lecture séquentielle   1 th :  4,1 Go/s |  8 th : 23,4 | 16 th : 28,7 | 32 th : 28,2
 *   dispersion pure        1 th : 0,96 Gév/s|  8 th : 3,46 | 16 th : 3,20 | 32 th : 3,22
 *   écarts + dispersion    1 th : 0,87 Gév/s|  8 th : 4,55 | 16 th : 7,79 | 32 th : 6,79
 *
 * Enseignements :
 *  - la machine plafonne à ~29 Go/s (population mémoire limitée), pas 100 ;
 *  - la dispersion sature vers 8 threads (~3,5 G év/s) : c'est l'accès aléatoire
 *    à l'accumulateur qui limite, pas la bande passante ;
 *  - le décodage par écarts est quasi gratuit (le noyau complet va PLUS vite que
 *    la dispersion pure, grâce au flux séquentiel des deltas).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <omp.h>

static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+1e-9*t.tv_nsec; }

#define NOUT 4096
#define NEV  (50u*1000u*1000u)   /* 50 M événements */

int main(void){
    /* ---------- 1. bande passante lecture (multi-thread) ---------- */
    size_t NF = 64u*1024u*1024u;              /* 64 M floats = 256 Mo */
    float *a = aligned_alloc(64, NF*sizeof(float));
    for(size_t i=0;i<NF;i++) a[i]=1.0f;
    printf("=== bande passante lecture séquentielle ===\n");
    for(int th=1; th<=32; th*=2){
        omp_set_num_threads(th);
        double t0=now(); double s=0;
        #pragma omp parallel for reduction(+:s) schedule(static)
        for(long i=0;i<(long)NF;i++) s+=a[i];
        double dt=now()-t0;
        printf("  %2d threads : %6.1f Go/s   (somme=%.0f)\n", th, NF*4.0/dt/1e9, s);
    }
    free(a);

    /* ---------- 2. dispersion pure : acc[dest] += v ---------- */
    uint32_t *dest = malloc((size_t)NEV*sizeof(uint32_t));
    float    *val  = malloc((size_t)NEV*sizeof(float));
    uint32_t rng=12345;
    for(size_t i=0;i<NEV;i++){ rng=rng*1103515245u+12345u; dest[i]=(rng>>8)%NOUT; val[i]=(float)((int)(rng>>16)%2?1:-1); }
    printf("\n=== dispersion acc[dest] += v (accumulateurs par thread) ===\n");
    for(int th=1; th<=32; th*=2){
        omp_set_num_threads(th);
        float *acc = calloc((size_t)th*NOUT, sizeof(float));
        double t0=now();
        #pragma omp parallel
        {
            int id=omp_get_thread_num();
            float *my=acc+(size_t)id*NOUT;
            #pragma omp for schedule(static)
            for(long i=0;i<(long)NEV;i++) my[dest[i]] += val[i];
        }
        double dt=now()-t0;
        double chk=0; for(int i=0;i<th*NOUT;i++) chk+=acc[i];
        printf("  %2d threads : %6.2f G événements/s   (contrôle=%.0f)\n", th, NEV/dt/1e9, chk);
        free(acc);
    }

    /* ---------- 3. décodage par écarts + dispersion (le vrai noyau) ---------- */
    uint16_t *delta = malloc((size_t)NEV*sizeof(uint16_t));
    int8_t   *sgn   = malloc((size_t)NEV);
    for(size_t i=0;i<NEV;i++){ rng=rng*1103515245u+12345u; delta[i]=(uint16_t)(1+(rng>>9)%16); sgn[i]=(rng>>20)&1?1:-1; }
    printf("\n=== décodage d'écarts + dispersion (noyau réel) ===\n");
    for(int th=1; th<=32; th*=2){
        omp_set_num_threads(th);
        float *acc = calloc((size_t)th*NOUT, sizeof(float));
        double t0=now();
        #pragma omp parallel
        {
            int id=omp_get_thread_num();
            float *my=acc+(size_t)id*NOUT;
            /* chaque thread traite un segment ; l'index cumulatif redémarre au segment */
            long chunk=(long)NEV/th;
            long beg=(long)id*chunk, end=(id==th-1)?(long)NEV:beg+chunk;
            uint32_t idx=0;
            for(long i=beg;i<end;i++){ idx=(idx+delta[i])%NOUT; my[idx]+=sgn[i]; }
        }
        double dt=now()-t0;
        double chk=0; for(int i=0;i<th*NOUT;i++) chk+=acc[i];
        printf("  %2d threads : %6.2f G événements/s (+décodage)  contrôle=%.0f\n", th, NEV/dt/1e9, chk);
        free(acc);
    }
    free(dest); free(val); free(delta); free(sgn);
    return 0;
}
