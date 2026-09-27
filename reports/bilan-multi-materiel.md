# Bilan multi-matériel — CPU, FPGA, GPU

État au terme des trois implémentations. Tous les chiffres marqués **mesuré** ont
été pris sur cette machine, avec le code de ce dépôt ; ceux marqués *projeté* ou
*déduit* le sont explicitement, avec leur base.

Machine : 2 × Xeon E5-2687W v3 (20 cœurs / 40 threads, 125 Go), 2 × Quadro
RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak,
DDR3 9,66 Go/s, PCIe Gen3 ×8 6,5 Go/s, QSFP+ 4,8 Go/s).

Modèle de référence pour toutes les comparaisons : **Qwen2.5-0.5B-Instruct Q8_0**,
494 M de poids, 4 864 dimensions cachées, 24 couches. Un token = **352,8 M
d'événements** (0,7 Go de listes lues).

---

## 1. Ce qui a été construit

| Cible | Livrable | Taille | Vérification |
|---|---|---|---|
| **CPU** | `qtrinet-core` — moteur d'événements, tokenizer BPE, forward Qwen2, génération, perplexité | **2 547 lignes de Rust, `std` seul, 0 dépendance** | tokens identiques à la référence numpy ; perplexité identique ; 14/14 au banc des décodeurs |
| **FPGA** | `event_pe.sv`, `event_engine.sv`, `event_reader.sv` + bancs + modèle DDR3 + empaqueteur | **1 924 lignes** | 309 020 événements réels, aucune divergence (PE, lecteur, réduction) ; synthétisé sur la vraie puce |
| **GPU** | micro-bancs des deux primitives (bande passante, dispersion) | ~80 lignes Numba | mesuré sur les cartes |

Outillage reconstruit au passage : **iverilog 13.0 compilé depuis les sources**
(flex puis iverilog) — c'est ce qui débloque la vérification RTL sans licence
Questa ; chaîne Quartus Prime Standard 21.1.1 opérationnelle sur le vrai device.

## 2. Performances mesurées et déduites

### Un token du 0,5 B Q8

| Implémentation | ms/token | tok/s | Statut |
|---|---|---|---|
| numpy float32 + OpenBLAS (40 threads) | 132 | 7,6 | mesuré |
| CPU, moteur d'événements (push) | 64 | 15,6 | mesuré |
| **CPU, noyau dense int8 (pull)** | **27** | **36,4** | **mesuré — après correction du produit scalaire** |
| FPGA, 1 carte, 51 voies | ~73 | ~13,7 | *projeté* (PE et lecteur vérifiés et synthétisés) |
| GPU, mode listes (atomics) | ~19,5 | ~51 | *déduit* de la dispersion mesurée |
| **GPU, dense int8** | **~1,3** | **~770** | *déduit* de la bande passante mesurée |

### Le débit par événement, et son coût énergétique

| Ressource | Débit | Énergie par événement (TDP) |
|---|---|---|
| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |
| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |
| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |

### Montée en charge

| Ressource | Courbe mesurée |
|---|---|
| CPU | 1 thread 0,41 G → 8 : 2,75 → 16 : 4,45 → **32 : 5,3** G évts/s ; effondrement à 39+ |
| FPGA | 1 événement/cycle/voie, **0,86 mesuré** avec le lecteur ; optimum à 32 PE pour le banc seul (177 MHz) |
| GPU | 18,1 G évts/s de dispersion, 380 Go/s de lecture |

## 3. Ce que l'architecture événementielle apporte réellement

1. **Les listes sont portables.** Les mêmes octets nourrissent le CPU, le FPGA et
   le GPU. Aucune des trois implémentations n'a nécessité de reformater les
   données — c'est ce qui rend un hybride bon marché.
2. **Ce qui circule, ce sont les activations.** 896 × 2 octets par matrice, soit
   **3,5 Mo par token** sur PCIe (0,5 ms) contre 63 à 95 ms de calcul. Les poids
   ne bougent jamais : les kilo-octets traversent, pas les méga-octets.
3. **Pas de multiplieur requis.** Le PE atteint 112,5 MHz avec 176 ALMs **et zéro
   DSP**, contre 115 ALMs et 1 DSP avec multiplieur — et **pas un hertz d'écart**.
   La contrainte du CDC est tenue sans pénalité de fréquence.
4. **Les adresses strictement croissantes** des listes suppriment tout aléa
   d'accumulateur : le pipeline tient 1 événement/cycle sans contournement.
5. **Le coût suit le nombre de non-zéros**, pas la largeur des valeurs. Conséquence
   mesurée : passer de 8 à 4 bits ne rapporte que 11 % de mémoire et 12 %
   d'événements, pour 12 % de perplexité en plus.

## 4. Ce qui n'est PAS construit

| Manque | Conséquence |
|---|---|
| **Rien n'a tourné sur la carte** | JTAG validé, bitstream produit, mais le moteur d'événements n'a jamais été programmé. Tous les chiffres FPGA sont simulation + synthèse. |
| **Pas de contrôleur DDR3** | Le lecteur est éprouvé contre un modèle à latence fixe ; un vrai contrôleur a banques, rafraîchissements et reprises. |
| **Pas de séquenceur** | Rien ne parcourt les 168 matrices d'un modèle. |
| **Pas de chemin retour** | Accumulateur → liste d'activations de la couche suivante : inexistant. |
| **Aucune opération non matricielle en RTL** | RMSNorm, RoPE, softmax, SiLU, résidus : code hôte en float. |
| **Attention hors du domaine événementiel** | Ses poids sortent d'un softmax calculé à l'exécution : non pré-stockables. Et elle croît **linéairement** avec le contexte (2,0 ms à 64 tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192). |
| **Multi-cartes** | Rien d'implémenté ; le ring QSFP+ est une projection. |
| **Modèle ternaire entraîné** | Tout repose sur de la quantification après coup (PTQ). |

## 5. Corrections de mes propres affirmations

| Affirmation | Statut |
|---|---|
| « Encodage hybride ×2,17 » | **Retirée** — le code proposé viole l'inégalité de Kraft (Σ2^−l = 1,992 > 1) |
| « Fusion divergente au rang 0 » et « 7,53 G évts/s » | **Fausses** — un état partagé à deux contrats de nettoyage ; valeurs réelles 3,66 / 4,99 G |
| Perplexité 20,29 (harnais Python) | **Invalidée** — `bpe_np.py` s'écarte du vrai pré-tokenizer Qwen2 sur 5 points (5,2 % d'identifiants). Le tokenizer Rust est conforme 737/737 ; la mesure est à reprendre |
| « 27 PE suffisent, 3 % de la logique » | **Corrigée** — en comptant le lecteur : 51 voies, 41 % de la logique et 41 % de la M20K |
| « Le mode liste coûte 8 % face au dense » | **Périmée** — après suppression de la liste des destinations touchées, il est **8 % plus rapide** que le dense (15,8 contre 14,7 tok/s) |
| « Le FPGA n'a pas NVLink / les RTX 5000 non plus » | **Corrigée** — l'utilisateur avait raison, 25,78 Go/s mesurés par lien |
| « L'architecture convertit la sparsité en vitesse » | **Nuancée** — 10× moins d'événements ne donnent que 2× de vitesse (localité du scatter et taille d'accumulateur) |

## 6. Verdict par ressource

**CPU — la référence, et elle tient.**
15,8 tok/s sur un 0,5 B quantifié, en arithmétique entière, sans BLAS, sans GPU,
sans dépendance : le moteur d'événements **bat maintenant le noyau dense** sur la
même machine. Il reste 2,8× de marge avant la limite mémoire (10,4 Go/s utilisés
sur 28,7). C'est l'implémentation la plus aboutie des trois.

**FPGA — vérifié, synthétisé, et pas compétitif sur le débit.**
Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 %
de la mémoire embarquée. Son argument réel est l'**énergie par événement**
(8,3 nJ contre 57 pour le CPU, soit 7×) et l'absence de multiplieur. Face au GPU
elle est **38× plus lente** sur les mêmes données, parce que sa DDR3 fait 9,66 Go/s
contre 380 Go/s.

**GPU — il gagne sur les trois axes.**
Plus rapide (51 tok/s en mode listes, ~770 en dense), meilleur par événement que
le CPU (12,7 contre 57 nJ), et il consomme les mêmes listes. **Il n'y a pas de
régime, sur cette machine, où le FPGA batte le GPU** : les deux lisent les mêmes
octets, et le GPU lit 39× plus vite.

**Hybride — justifié, mais pas comme prévu.**
Le bon découpage, mesuré : **GPU** pour l'attention, les normes, la tête et
l'échantillonnage (dense, dépendant des données) ; **CPU** pour l'orchestration et
les 125 Go de mémoire ; **FPGA** seulement hors du régime « avec GPU », ou comme
tranche mémoire pour un modèle qui ne tient pas dans 16 Go (sa DDR3 bat le PCIe
de 1,5×). La communication n'est pas l'entrave — c'est le seul point du cahier des
charges que les listes d'événements règlent vraiment.

## 7. Le prochain pas le plus rentable

Ni le FPGA ni le GPU : **les 2,8× qui restent sur le CPU**, en tuilant la dimension
de sortie pour garder l'accumulateur dans le L1 (leçon tirée du mode épars, où
ajouter des threads *ralentissait* : 31 ms à 4 threads contre 53 à 32). Ce gain ne
demande aucun matériel, et il porterait le moteur à ~40 tok/s — au niveau du GPU en
mode listes, sans GPU.

## 8. Reproductible

```bash
# CPU
cd qtrinet-core && cargo build --release
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --ids 9707,0 --n 16 --threads 16 --abits 16
./target/release/qtrinet-core ../models/Qwen2.5-0.5B-Q8_0.gguf --threads 16   # banc des décodeurs

# FPGA (aucune licence)
export PATH=$HOME/iverilog/bin:$PATH
cd ../FPGA-Stratix-V
python3 tools/pack_lists.py <modele.gguf> blk.0.ffn_gate.weight --sources 64 --out sim
iverilog -g2012 -o /tmp/sim_rd rtl/event_reader.sv rtl/event_pe.sv tb/ddr3_model.sv tb/tb_event_reader.sv
vvp /tmp/sim_rd
source tools/quartus_env.sh && quartus_sh --flow compile syn/reader/event_reader
```
