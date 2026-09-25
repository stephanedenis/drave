# Moteur d'événements Rust — les 4 optimisations, et les 3 pièges

Moteur `qtrinet-core` (Rust, **std seul**, zéro dépendance, 386 lignes de moteur).
Matrice réelle `blk.0.ffn_gate.weight` de Qwen2.5-0.5B-Q8_0 : 4864 entrées × 896
sorties, **4 303 745 événements** (ternaire issu des signes réels, densité 100 %).
Machine : 2 × Xeon E5-2687W v3 (20 cœurs / 40 CPU logiques), NUMA 2 nœuds.

---

## Les 4 optimisations

### 1. Réduction incrémentale (fin du memset)

Chaque worker ne remet à zéro **que les destinations qu'il a touchées** ; le
demandeur ne réduit que la fenêtre réellement écrite. Coût d'un appel à vide :
**0,484 ms → 0,011 ms** (×44). C'est ce qui rend le débit *variable* exploitable :
un événement rare ne paie plus le prix d'un appel plein.

### 2. Décodage SWAR par paquets de 8

Les écarts d'un octet (99,99 % des événements à forte densité) sont décodés **8 à
la fois dans un mot de 64 bits** : un seul test `w & 0x8080_8080_8080_8080` dit si
les 8 octets sont des varints d'un octet ; les valeurs sortent par décalages, sans
branche par élément.

### 3. Vecteur d'activation creux explicite (`SparseVec`)

La cascade produit directement `(indices triés, valeurs contiguës)` — 8 octets par
source active. Plus aucun test de zéro ni accès indirect au tableau dense dans la
boucle chaude. C'est aussi la structure que produira le matériel.

### 4. Listes fusionnées (`FusedSign`)

Une **seule** liste triée par destination + plan de signe, au lieu de deux listes
(+, −) : l'accès à l'accumulateur devient **monotone**, en une passe.

Coût : 4,89 Mo (8,97 b/poids) contre 4,34 Mo (7,98 b/poids) pour les deux listes
séparées. Le bitmap+signe reste à 1,09 Mo (1,99 b/poids), mais impose un parcours
dense, donc un débit **constant** — exactement ce qu'on veut éviter.

---

## Résultats (30 threads, réglage par défaut)

| Densité | Événements | Fusion | 2 listes |
|---|---|---|---|
| 0 % | 0 | 0,011 ms | 0,011 ms |
| 1 % | 43 560 | 0,14 G év/s | 0,42 G év/s |
| 5 % | 216 960 | 1,15 G év/s | 1,50 G év/s |
| 10 % | 430 359 | 1,81 G év/s | 2,30 G év/s |
| 25 % | 1 076 785 | 3,18 G év/s | 3,86 G év/s |
| 50 % | 2 152 648 | 4,14 G év/s | 4,89 G év/s |
| 100 % | 4 303 745 | **4,51 G év/s** (0,95 ms) | **5,44 G év/s** (0,79 ms) |

**Exactitude : 14 vérifications sur 14** — les deux décodeurs donnent le résultat
exact du produit matrice-vecteur dense de référence, **à chacune des 7 densités**
(le harnais ne validait qu'une seule densité auparavant : c'est précisément la
remise à zéro et la fenêtre de réduction qui dépendent de la densité).

Le débit varie de **0,011 ms à 0,95 ms sur la même matrice** (rapport 86) selon ce
qui s'active : « on ne paie que ce qui s'active » est vérifié à l'échelle du moteur.

## Montée en charge (meilleur de 3 passes, densité 100 %)

| Threads | 1 | 2 | 4 | 8 | 16 | 28 | 32 | **39** |
|---|---|---|---|---|---|---|---|---|
| Fusion (G év/s) | 0,41 | 0,75 | 1,45 | 2,75 | 4,45 | 4,35 | **4,84** | 2,04 ❌ |
| 2 listes (G év/s) | 0,42 | 0,78 | 1,49 | 2,83 | 4,37 | 5,24 | **5,78** | 2,59 ❌ |

➡️ **~0,15–0,18 G év/s par thread**, optimum vers 28–32 threads, soit ~0,8–1,3
événement par cycle CPU. Une carte à 124 MHz × 32 PEs = 4 G év/s vise donc
**exactement un CPU 16–32 cœurs** : le FPGA n'apporte pas la cadence brute, il
l'apporte par watt et par carte.

> Mesures prises avec le bureau actif (load ~1,5–5) : ±20 % d'une passe à l'autre,
> d'où le « meilleur de 3 ». Le moteur refuse désormais de dépasser `CPU − 1` et
> prend `3/4 × CPU` par défaut.

---

## Les 3 pièges (chacun a coûté une campagne de mesures fausses)

### Piège 1 — un état partagé, deux contrats de nettoyage

La première campagne annonçait « fusion DIVERGENTE au rang 0 : 3838 vs 3513 » et un
chemin 2-listes à 7,53 G év/s. **Les deux chiffres étaient faux.** Le chemin
« 2 listes » vidait l'accumulateur par un `memset` complet **puis vidait la liste
des destinations touchées** : l'appel fusion suivant ne trouvait donc rien à
effacer et **accumulait sur les restes de l'appel précédent**.

> **Leçon** : quand deux implémentations partagent un état, le contrat de nettoyage
> doit vivre dans l'état partagé, pas dans la convention de l'appelant.
> `row_delta_into` prend maintenant `touched` en paramètre, comme la version fusion.

La même leçon vaut pour la **fenêtre de réduction** : la déduire de la liste
`touched` était faux dès que cette liste débordait (elle est bornée à `n_cols`).
Les deux fonctions de ligne retournent maintenant l'**étendue exacte** des
destinations écrites (première et dernière colonne, tenues en registres), et la
réduction est l'union de ces étendues — exacte par construction, quel que soit le
décodeur.

### Piège 2 — `&mut` dans la boucle chaude

Suivre l'étendue via un `&mut (usize, usize)` passé à la fonction de ligne a fait
**chuter le débit de 3,09 à 0,97 G év/s** (8 threads) : le compilateur ne peut plus
prouver que ce pointeur n'alias pas `acc`, et doit recharger/restocker à chaque
événement. Le suivi tient désormais dans **deux variables locales**, écrites une
seule fois, à la sortie de la fonction : débit retrouvé, exactitude en plus.

> **Leçon** : dans une boucle à 4 M d'itérations, un pointeur `&mut` de plus n'est
> pas « gratuit » — c'est une barrière d'aliasing, pas un registre.

### Piège 3 — attente active et sursouscription

À **39 workers + le thread appelant sur 40 CPU logiques**, le débit s'effondre :
**4,84 → 2,04 G év/s**. Les workers qui tournent ne rendent jamais la main ;
l'ordonnanceur préempte un thread qui *spin*, et la barrière attend alors tout un
quantum avant qu'il revienne. Le reste du système (bureau) est affamé et se
ressert, ce qui aggrave la préemption.

La correction évidente — `yield_now()` après N tours — **a tout empiré** (0,97 G à
8 threads) : `sched_yield` est un appel système, et un worker qui attend 1 ms en
appelle des milliers. La bonne réponse est de **ne pas sursouscrire** : le pool est
borné à `CPU − 1` et la valeur par défaut est `3/4 × CPU`. Une barrière par *spin*
exige que tous ses threads soient résidents **simultanément**.

> **Leçon** : une barrière par attente active est un contrat avec l'ordonnanceur.
> Si on ne peut pas garantir la résidence, il faut une barrière bloquante — mais
> elle coûte des microsecondes, ce qui tue le débit variable. Ici, on préfère
> borner la taille du pool.

---

## Exécution sans multiplieur

| | temps | ops |
|---|---|---|
| multiplication i8×i8 | 2,5 ms | 4,36 M |
| **décalages + additions** | **112,3 ms** | 13,58 M (3,12 additions/poids) |
| rapport | **×44,9** | — |
| résultat | **identique** ✅ | — |

Les niveaux Q8_0 réels ont en moyenne 3,12 bits à 1 ⇒ ~3 additions par poids. Sur
CPU le multiplieur gagne 45× ; **sur FPGA il n'existe pas**. La contrainte du CDC
(« aucun DSP ») est donc satisfaite pour un modèle 8 bits, sans réentraînement ni
élagage.

---

## Ce que ça change pour le CDC

1. **Le débit est bien variable** : 0,011 ms à vide, 0,95 ms à pleine activation.
   L'argument « on ne paie que ce qui s'active » est vérifié à l'échelle du moteur,
   pas seulement en théorie.
2. **3–5 G év/s sur un CPU de bureau**, soit ~1 événement par cycle. Un banc
   FPGA à 124 MHz × 32 PEs taperait 4 G év/s — la carte gagne par le watt, pas par
   la cadence.
3. **Ni tri, ni dédoublonnage** : l'ordre naturel des écarts suffit (cf.
   [`rapport-cpu-aer.md`](rapport-cpu-aer.md)).

## Reste à faire

- **Traitement par blocs de destination** pour vectoriser : AVX2 n'a ni gather ni
  scatter entier, il faut transposer le parcours, pas la boucle.
- **Fusion par compartiments de destination** (réseau de combinaison façon routeur
  AER) : le seul dédoublonnage justifié, pour le multi-cartes.
- **Tolérance à la sursouscription** : barrière hybride (spin court + futex) si le
  moteur doit cohabiter avec d'autres charges.
