# A2.6 — reconnaissance : les experts et la tête du moteur

> **Ligne de roadmap** : A2.6 (ordonnanceur : experts et tête) · **Date** : 2026-11-18
> · **HEAD** : `bb57604c` · **Binaire mesuré** : `drave-core/target/release/drave`, 2026-11-17 14 h 21
> · **Nature** : **reconnaissance en lecture seule** — aucun fichier du moteur modifié, aucun commit.
> **Machine** : 2 × Quadro RTX 5000 (16 384 Mio), 125 Go de RAM, 40 fils ; **charge 13,7 → 31,4**
> pendant les mesures (d'autres sessions lisaient un modèle lourd) → les **temps absolus** sont
> bruités, les **écarts** de ×2 à ×5 ne le sont pas. Toute reprise doit se faire **machine au repos**.
>
> **Verdict** : A2.6 n'est **pas** bloquée par A6.2, et sa fiche est en retard de deux mesures.
> La règle existe (`placement.rs`, **8** tests, pas 4) mais elle n'est **le chemin de décision
> d'aucun opérateur sauf le KV** ; les experts et la tête sont placés par des **drapeaux et des
> seuils codés en dur**. Le chiffre qui manque n'est pas le débit des experts — il est mesuré ici
> à **5,6 Go/s** — c'est **la bande que la règle doit porter** : trois tables de bandes coexistent
> et donnent, pour le même opérateur, 35 ms ou 313 ms par jeton.

## 1. Ce qui existe

### 1.1 La règle, et où elle est appliquée

`drave-core/src/placement.rs` (253 lignes) :

| objet | ligne | état |
|---|---:|---|
| `BANDE_VRAM` 84,9 Go/s · `BANDE_RAM` 22,5 · `BANDE_NVME` 3,5 · `BANDE_RESEAU` 0,03125 | 21-27 | constantes mesurées le 24/10 (`rapport-placement-kv-8k.md`) |
| `Support` + `bande()` + `nom()` | 33-60 | 4 supports |
| `cout(octets_par_jeton, support)` | 64 | **octets ÷ bande**, sans réutilisation ni nombre de lecteurs |
| `classement(octets_par_jeton)` | 69 | tri par coût |
| `kv_en_vram` | 79 | KV + réserve ≤ VRAM libre |
| `choisir` | 90-103 | le moins cher où ça tient ; **retombe sur `Support::Nvme`** si rien ne tient |
| `Precision` / `PRECISIONS` (f32, int8 tardif, int4 tardif, **tête 4 bits +10 %**, int4 global +364 %) | 107-127 | table de précisions, **aucune entrée tête Q6_K/Q8_0** |
| `choisir_avec_perte` | 136-158 | place **et** perte sous `perte_max` |
| `perte_kv_int8` / `kv_precision` | 163-174 | int8 par couche (A5.3) |
| **8 tests** | 176-253 | `cargo test placement` |

**Sites d'appel réels** (grep `placement::`) :

| site | ce qu'il décide |
|---|---|
| `model.rs:4720` `kv_precision` | la précision du KV couche par couche, **sous `DRAVE_PERTE_MAX`** (opt-in, A8.3) |
| `model.rs:4889` `kv_en_vram` | le miroir VRAM du KV, **sous `DRAVE_GPU_KV`** ; seul endroit du dépôt qui imprime un **refus nommé** (« KV déporté REFUSÉ par la règle de placement ») |
| `model.rs:4988` `choisir` | la tête : le choix est **calculé puis jeté** (`let _tete_tient = …`) — le commentaire dit pourquoi (place ≠ qualité) |
| **—** | **aucun appel pour les experts** |

### 1.2 Le placement réel : drapeaux et seuils, pas la règle

| opérateur | ce qui décide **aujourd'hui** | lieu |
|---|---|---|
| projections | seuil **codé en dur** `SEUIL_GPU = 8 Mio`, Q8_0 seulement, **GPU en auto** | `model.rs:1959-1977` |
| KV | `DRAVE_GPU_KV` (opt-in) + la règle | `model.rs:4882-4905` |
| tête | `DRAVE_GPU_TETE` (opt-in) ; 4 bits = `--q4-tout` (seul à poser le bit `4` de `q4`), pas de drapeau isolé | `model.rs:4859-4885`, `main.rs:1696-1699` |
| cache VRAM des experts | `DRAVE_GPU_EXPERTS` + `DRAVE_GPU_EXPERTS_GO`, **défaut = VRAM libre − 2,0 Go** | `model.rs:4956-4972` |
| cache RAM des experts | `DRAVE_EXPERTS_RAM` en Mo, aucun défaut (mesuré perdant) | `model.rs:5053-5075` |
| taille du cache d'experts dans le plan | `vram − 2,0 (réserve CUDA) − 8,0 (commun)` | `materiel.rs:350-360` |
| prélecture des experts | `DRAVE_PRELIRE_FILS` / `DRAVE_TAMPONS_FILS`, 8 fils par défaut | `gguf.rs:348-350`, `model.rs:8432-8472` |
| plan « machine » | `materiel::plan` + `cout_par_jeton` : **imprimés**, jamais appliqués | `main.rs:3637-3661` |

Deux **tables de bandes** de plus, qui ne disent pas la même chose que `placement.rs` :

| table | VRAM | RAM | NVMe | réutilisation |
|---|---:|---:|---:|---|
| `placement.rs:21-25` | 84,9 | 22,5 | **3,5** | non |
| `materiel.rs:406-411` | 84,9 | 22,5 (**jamais utilisée**) | **31,0** (16 lecteurs) | `SUCCES = 0,80` |
| `tools/budget_execution_locale.py:39-47` | — | 9,6 (1 fil) / 40 (8 fils) | 2,3 (1 flux) / 3,4 (4 flux) | non |

Pour l'opérateur experts du MoE local (**1,097 Go par jeton**), ces tables donnent **313 ms** (3,5),
**49 ms** (22,5), **35 ms** (31,0, avec 80 % de succès) — mesuré : **195 ms** (§ 1.4).

### 1.3 Le chemin des experts dans le moteur — bien plus complet que la fiche ne le dit

| brique | lieu | état |
|---|---|---|
| convention de routage lue du GGUF (softmax, sigmoïde, racine de softplus, gpt-oss) | `model.rs:26-46`, `Routage` 306-311, `routage_du_gguf` 320-369 | fait, **quatre familles** (softmax, sigmoïde, top-k brut puis softmax, racine de softplus) |
| sélection unique (jeton **et** lot), biais, `tid2eid`, échelle | `router` 490-580, `choix_experts` 482 | fait |
| élision par fréquence (`DRAVE_EXPERTS_GARDES`) | 398-430 | fait, mesuré (`rapport-morcellement-experts.md`) |
| trace de routage (`DRAVE_TRACE_EXPERTS`, `_ORDRE`) | 432-460, `trace_experts` 2896-2900 | fait |
| routage imposé (`DRAVE_ROUTAGE_FORCER`), invariant exact | 432-480 | fait, porte `porte-echange-experts` |
| `charger_moe` : tenseurs empilés, clusters, expert partagé, forme creuse | 817-1057 | fait |
| `Moe` (routeur, biais, `tid2eid`, `Vue4`, masque, mapping) | 1504-1553 | fait |
| `Moe::ou` (expert global → vue, ligne locale) | 1555-1570 | fait |
| **cache RAM** des experts (LRU, budget en Mo) | 1583-1700 | fait, **mesuré plus lent** |
| **cache VRAM** des experts (LRU, pool de tampons, MXFP4) | 1983-2100 | fait, **MXFP4 seulement** |
| garde de format du cache VRAM | `model.rs:8486` `if moe.gate[0].src == Source::Mxfp4` | Q4_K/Q6_K **ne passent pas** : CPU |
| prélecture / `pread` par tranches (`DRAVE_TAMPONS`) | `gguf.rs:326-420`, `model.rs:8432-8472` | fait (8 fils) |
| profilage par provenance (`proj+mlp`) | `model.rs:8607` (MoE) et `8676` (dense) ; impression `main.rs:2141` | fait |
| noyau GPU Q4_K d'expert | mesuré 0,171 ms/matrice, **5,17 Go/s** (`rapport-vram-transfert.md`) | **non branché** en production |

### 1.4 Ce qui est mesuré, et où

| mesure | valeur | source |
|---|---|---|
| fichier, architecture | 18 556 686 752 o · 579 tenseurs · 48 couches · **128 experts, 8 par jeton** · FFN expert 768 | `--tensors`, `--config` |
| experts (toutes couches) | **17,55 Go** · **2,86 Mo/expert** (3 matrices) | `analyse_octets_par_jeton.py --experts-par-jeton 8` |
| **octets d'experts par jeton** | **1,097 Go** (17,55 / 16) | idem |
| **coût mesuré des experts** (`proj+mlp`), 7 jetons notés | **194,8 ms/jeton** à 8 fils, 279,1 à 4, 188,8 à 16 → **≈ 5,6 Go/s** | ce rapport, § 3 |
| même, en `DRAVE_TAMPONS=1` | 362,8 ms (8 fils) — **1,9× plus lent** | ce rapport |
| même, avec `DRAVE_EXPERTS_RAM=4096` | **567,9 ms** — le cache RAM est le plus lent | ce rapport + `model.rs:1583` |
| perplexité (contrôle d'invariance) | **799,8557** à l'identique sur tous les chemins | ce rapport |
| réutilisation | 46,9-48,8 % immédiate ; **LRU 32/128 → 74,8-87 %** ; 64/128 → 92-93 % | `rapport-reutilisation-experts.md` § 2 |
| regroupement par expert au lot | 192 : 74 496 → 4 804 lectures (**÷15,51**), temps **×1,58** ; 64 : ÷7,08 ; 8 : ÷2,27 | `rapport-prefill-par-experts.md` § 1-2 |
| découpage en 8 clusters | 3,08 nœuds contre 5,32 au hasard (**÷1,73**), couverture 0,607 | `rapport-decoupage-moe.md` |
| cache VRAM (plafond) | **×1,09** pour Kimi-K3 (28,7 % de succès), plafond absolu ×1,41 ; **Q4_K non câblé** | `rapport-cache-experts-vram.md`, `rapport-coordination-a.md:73` |
| C9 / routage | 37,2013 (limit 32) ; porte **54,5202** à N=16, invariant exact | `rapport-coordination-a.md` § 1.2 |
| tête 4 bits | **+10 %** de PPL (30,7660 → 33,8230, 0,5 B, 255 jetons) — **historique, non rejouable isolément** : `--q4-tout` quantifie aussi attention et FFN (+40,8 % mesuré ici) | `rapport-placement-kv-8k.md` ; ce rapport |
| **tête Q8_0 en VRAM** (mesuré ici) | PPL **56,7642 → 56,7642** ; tête **7,43 → 1,80 ms/jeton** (÷4,1) ; 24,6 → 28,4 tok/s | ce rapport, § 3.4 |
| contrôle négatif tête | `DRAVE_GPU=0` : pas de ligne `[gpu]`, PPL 56,7642, tête **7,75 ms** | ce rapport |

**Drapeaux périmés** : `gpu::instance()` est passé en **AUTO** (`gpu.rs:1582-1591` : le GPU est
essayé par défaut, `DRAVE_GPU=0` force le CPU) alors que son commentaire (1549) et
`rapport-drapeaux-ignores.md` § 5 disent encore « sans `DRAVE_GPU`, aucune ressource vidéo ». Vérifié :
`DRAVE_GPU_TETE=1` **seul** active la tête GPU.

## 2. Ce qui manque pour clore A2.6 (précisément)

1. **L'objet « expert » dans la règle.** Aucun type, aucune fonction : `placement.rs` ne connaît que
   des octets et un support. Il manque `cout`**`_experts`** (ou un `Operateur` générique) prenant
   `octets_par_jeton`, `taux_succes`, `lecteurs`, et rendant support + coût + **raison**.
2. **Le refus nommé.** `choisir` **ne peut pas refuser** : il retombe sur `Support::Nvme` (l. 96-102),
   et le test `choisir_respecte_la_place` (l. 199-206) **exige** ce repli. Le contrat de la fiche
   (« un opérateur qui ne tient nulle part : refus nommé, pas de placement silencieux ») n'est donc
   pas tenu — seul le KV a un refus imprimé, codé à la main dans `model.rs:4889`.
3. **La bande de l'opérateur experts.** Mesurée **5,6 Go/s** (§ 3) ; aucune constante ne la porte.
   Sans elle, la règle place au hasard entre 35 ms et 313 ms : **la mesure du § 3 est le préalable**.
4. **La réutilisation dans le coût.** 47 % de réutilisation immédiate, 87 % à LRU 32/128 : `cout()`
   lit tout, chaque jeton. `materiel::cout_par_jeton` a un `SUCCES = 0,80` en dur mais **n'est pas
   branché**. Il faut un seul modèle de coût, réutilisation comprise.
5. **La trace.** `classement`/`cout` ne sont **imprimés nulle part** ; la porte 3 de la fiche
   (« trace : le classement et le coût retenu sont imprimés et testés ») n'a ni code ni test.
6. **La reproductibilité.** Aucun test « mêmes entrées → même choix » (porte 3).
7. **La tête : une `Precision` au format du fichier.** `PRECISIONS` n'a que `TETE_4BIT` (+10 %).
   Le § 3.4 mesure une place à **perte nulle** (Q8_0/Q6_K sur VRAM) : il manque la constante
   (perte 0,0) et l'appel `choisir_avec_perte` — aujourd'hui le choix est calculé puis jeté
   (`model.rs:4988`).
8. **Les chiffres de la fiche.** 4 tests (il y en a **8**) ; « experts bloqués par A6.2 » (le MoE
   est là, et A6.2 est le **routage appris**, pas le placement) ; étape 2 ✅ *et* étape 4 ⏳ sur la
   tête alors que les deux décrivent le même refus ; « experts non mesurables » alors que
   `proj+mlp` les mesure depuis toujours.
9. **Le lot ≥ 2** : `rapport-a26-lot-disque.md` le dit assumé ; ce n'est pas un manque, c'est une
   décision déjà prise (PPL −0,006 %, +27 % de calcul).

## 3. La prochaine expérience : épingler la bande des experts

### 3.1 Ce qui a déjà été mesuré ici (à rejouer, machine au repos)

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
M="$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf"
IDS="$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt"

# 1. la reference : chemin mmap par defaut, 8 fils
./drave-core/target/release/drave "$M" --ppl "$IDS" --ctx 512 --limit 8 --threads 8 \
  | grep -E "postes|perplexit"
# 2. le controle : le cache RAM doit etre PLUS LENT (sinon la mesure est un artefact)
DRAVE_EXPERTS_RAM=4096 ./drave-core/target/release/drave "$M" --ppl "$IDS" \
  --ctx 512 --limit 8 --threads 8 | grep -E "postes|perplexit"
# 3. le chemin tampons doit etre plus lent aussi
DRAVE_TAMPONS=1 ./drave-core/target/release/drave "$M" --ppl "$IDS" \
  --ctx 512 --limit 8 --threads 8 | grep -E "postes|perplexit"
# 4. la saturation : 4, 8, 16 fils (meme graine, meme prompt)
for T in 4 8 16; do ./drave-core/target/release/drave "$M" --ppl "$IDS" \
  --ctx 512 --limit 8 --threads "$T" | grep postes; done
```

Résultats obtenus pendant cette reconnaissance (durée ≈ 13 s par point, **charge 13,7 → 31,4**) :

| réglage | `proj+mlp` (ms/jeton) | bande implicite (1,097 Go ÷ t) |
|---|---:|---:|
| défaut, 4 fils | 279,1 | 3,9 Go/s |
| **défaut, 8 fils** | **194,8** | **5,6 Go/s** |
| défaut, 16 fils | 188,8 | 5,8 Go/s |
| `DRAVE_TAMPONS=1`, 8 fils | 362,8 | 3,0 Go/s |
| `DRAVE_EXPERTS_RAM=4096`, 8 fils | **567,9** | 1,9 Go/s |

Perplexité **identique** (799,8557) sur tous les chemins : un placement change le temps, jamais le
chiffre — c'est l'invariance qui rend les temps comparables.

### 3.2 Le protocole à exécuter (10 points, ≈ 4 min sur une machine au repos)

Même commande, `--limit 32` (31 jetons notés) pour la statistique, et **deux passes** par réglage
(la première paie la lecture froide) :

```bash
for T in 4 8 16; do
  for P in 1 2; do
    ./drave-core/target/release/drave "$M" --ppl "$IDS" --ctx 512 --limit 32 --threads "$T" \
      2>&1 | grep -E "postes|perplexit"
  done
done
DRAVE_EXPERTS_RAM=4096 ./drave-core/target/release/drave "$M" --ppl "$IDS" --ctx 512 --limit 32 \
  --threads 8 2>&1 | grep -E "postes|perplexit"
DRAVE_TAMPONS=1 ./drave-core/target/release/drave "$M" --ppl "$IDS" --ctx 512 --limit 32 \
  --threads 8 2>&1 | grep -E "postes|perplexit"
```

**Chiffre attendu** : `proj+mlp` ≈ **195 ms/jeton** à 8 fils (5,6 Go/s), **pas** 49 ms (RAM 22,5) ni
313 ms (NVMe 3,5) ; ≈ 190 ms à 16 fils (saturation, donc **pas** de gain de calcul) ; 280 ms à 4 fils ;
perplexité **37,2013** partout (chiffre de la coordination, `--limit 32`) ; cache RAM et tampons plus
lents. La conclusion attendue : **la bande de l'opérateur experts est celle d'UN lecteur
(≈ 5,4-5,6 Go/s, la mesure de `mesurer_lecture_experts.py`), pas celle des 31 Go/s à 16 lecteurs
séquentiels** — la règle doit porter cette
bande-là (ou refuser de placer), et le levier est le **nombre de lecteurs / le regroupement**, pas
le support.

**Contrôle négatif** (trois conditions, dans cet ordre) :

1. **le mécanisme est actif** : le moteur imprime `128 par couche, 8 par jeton` et `48/48` couches
   d'experts — sinon `proj+mlp` ne mesure pas des experts ;
2. **le cache RAM dégrade** (567,9 ms > 194,8) : la bande mesurée n'est pas un artefact du cache
   de pages ; `DRAVE_TAMPONS=1` dégrade aussi (362,8) ;
3. **la perplexité ne bouge pas** : si un placement déplace la PPL, le placement a changé le
   **calcul**, et le temps n'est plus comparable.

**Ce qui pourrait rendre le chiffre faux** :

- **la charge** : 13,7 → 31,4 pendant ces mesures (d'autres sessions lisent DeepSeek-V4.1, 366 Go) ;
  les valeurs absolues peuvent bouger de ±20 %, les rapports ×1,9 et ×2,9 non ;
- **le cache de pages** : 17,55 Go d'experts sur 125 Go de RAM ; si le fichier est chaud, la bande
  mesurée est celle de la RAM, pas du disque — d'où les deux passes et l'éviction
  (`posix_fadvise(DONTNEED)`, `tools/mesure_lot_disque.sh`) ;
- **`--limit 8` est court** (7 jetons) : le premier jeton paie la lecture froide ; `--limit 32`
  dilue cet effet, c'est pourquoi le protocole le demande ;
- **`proj+mlp` n'est pas que les experts** : il inclut le routeur et les normes (quelques %) ;
- **le noyau Q4_K du GPU n'est pas câblé** : aucune mesure de VRAM n'est possible sur ce modèle
  aujourd'hui (garde `Source::Mxfp4`, `model.rs:8486`), donc « le cache VRAM ne paie pas » **n'est pas
  démontré ici** — seul le plafond K3 (×1,09) l'est, et il ne se transpose pas (K3 a 55 % de dense
  dans son trafic, le 30B a 95 % d'experts).

### 3.3 La décision que cette mesure tranche

| si… | alors l'implémentation A2.6 est… | diff |
|---|---|---|
| `proj+mlp` sature à 8 fils (≈ 195 ms) | **la bande `experts` entre dans `placement.rs`** (5,6 Go/s), avec `lecteurs` et refus nommé ; le levier est le regroupement (÷15,5 au lot 192), pas le support | ~120 lignes |
| `proj+mlp` divise par 2 à 16 fils | l'opérateur est **borné par le calcul** : la règle doit modéliser les paires/s, pas les octets/s ; placer ne sert à rien et la règle doit le **dire (refus nommé)** | ~60 lignes |
| la PPL bouge d'un chemin à l'autre | la mesure est invalide : un placement a changé le calcul (bug) | — |

### 3.4 Acquis au passage : la tête a une place à perte nulle (mesuré ici)

```bash
P="$HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt"
B=./drave-core/target/release/drave
$B models/Qwen2.5-0.5B-Q8_0.gguf --ppl "$P" --ctx 512 --limit 32 --threads 8              # CPU
DRAVE_GPU_TETE=1 $B models/Qwen2.5-0.5B-Q8_0.gguf --ppl "$P" --ctx 512 --limit 32 --threads 8  # VRAM
DRAVE_GPU=0 DRAVE_GPU_TETE=1 $B models/Qwen2.5-0.5B-Q8_0.gguf --ppl "$P" --ctx 512 --limit 32 --threads 8
```

| chemin | PPL | tête (ms/jeton) | tok/s |
|---|---:|---:|---:|
| CPU (défaut) | 56,7642 | 7,43 | 24,6 |
| VRAM (`DRAVE_GPU_TETE=1`, tête Q8_0 **du fichier**, aucune requantification) | **56,7642** | **1,80** | 28,4 |
| contrôle `DRAVE_GPU=0` | 56,7642 | 7,75 | 24,0 |
| `--q4-tout` (4 bits sur attention + FFN + tête) | 79,9488 (+40,8 %) | 6,50 | 42,4 |

- C'est l'**étape 4 de la fiche** (« une place qui ne coûte pas la PPL ») : support changé,
  **même précision**, donc même arithmétique (le noyau GPU est exact à 2e-7,
  `rapport-logits-gpu-vs-cpu.md`), PPL identique à 4 décimales.
- **Ce qui pourrait le rendre faux** : l'égalité n'est imprimée qu'à 4 décimales ; le +10 % de la
  fiche n'est **pas rejouable isolément** (il faudrait un `--q4-tete`) et `--q4-tout` est confondu
  (tout le modèle passe en 4 bits) ; la charge de la machine au moment des runs.
- **Ce qu'il faut en faire** : une `Precision` `TETE_FICHIER` (perte **0,0**) dans
  `placement.rs`, et `choisir_avec_perte` appelé pour la tête — sinon `_tete_tient` reste un calcul
  jeté.

## 4. Fichiers à modifier, et risque

| fichier | changement | taille | risque |
|---|---|---:|---|
| `drave-core/src/placement.rs` | `cout_experts` (octets, taux de succès, lecteurs) ; `BANDE_EXPERTS` = la valeur du § 3 ; `choisir` rendant un **refus nommé** (`Option<(Support, Precision, &'static str)>`) ; `TETE_FICHIER` (perte 0) ; 4-6 tests (dont un de reproductibilité) | **+100 à 150 lignes** | **`choisir` est appelé 2 fois** (`model.rs:4988`, tests) : changer sa signature est mécanique ; changer sa **sémantique** (refus au lieu de `Nvme`) casse le test 199-206, à réécrire — c'est le test qui **décrit** l'actuel « placement silencieux » |
| `drave-core/src/model.rs` | brancher la règle aux 3 endroits : tête (4859-4885, 4988), cache VRAM d'experts (4956-4972), cache RAM (5053-5075) ; imprimer le classement et le coût retenu | **+40 à 60 lignes** | **chemin de chargement** : une erreur ici casse tous les modes ; **le défaut ne doit pas bouger** (opt-in `DRAVE_PERTE_MAX`), cf. A8.3b : « un changement de défaut qui déplace les chiffres des portes ne se fait pas sans les épingler » ; `DRAVE_GPU_*` sont lus **avant** le refus, l'ordre compte |
| `drave-core/src/materiel.rs` | `plan()` délègue à la règle (au lieu de `vram − 2,0 − 8,0`) ; `cout_par_jeton` prend les bandes de `placement.rs` (aujourd'hui 3 tables) | **+20 à 30 lignes** | `plan()` n'est qu'un **imprimé** (`main.rs:3637`) : le risque est de **déplacer les chiffres affichés** que des fiches citent ; `cout_par_jeton` a `RAM` **mort** (l. 407) |
| `drave-core/src/gguf.rs` | rien à faire pour la règle ; `lecteurs` est déjà là (`DRAVE_TAMPONS_FILS`, 8) | 0 | — |

**Le total reste petit** (≈ 200 lignes) ; le risque n'est pas la taille, il est **le chemin de
chargement et le défaut**.

**Tests à relancer** :

- `cargo test placement` (**8/8** aujourd'hui ; 12-14 après) — ce sont les portes 1 et 2 de la fiche ;
- `cargo test` du crate (le chemin de chargement est touché) ;
- `bash tools/porte-flux.sh` (PPL épinglée, `DRAVE_PERTE_MAX`), `porte-pont`, `porte-coupe` : ce
  sont les trois portes du régime 1 % (A8.3a) que le moindre déplacement de défaut fait bouger ;
- `bash tools/porte-echange-experts.sh` (**18 Go, plusieurs minutes** — machine au repos) : il
  vérifie l'invariant du routage, donc qu'un placement d'experts n'a pas changé les experts choisis ;
- `python3 tools/verifie_backlog.py` (la frontière annonce encore A2.6) et
  `python3 tools/revue_documentation.py` ;
- **pas** `bash tools/toutes-les-portes.sh` (90 portes, 116 min) : la passe complète se décide en
  clôture, pas en cours d'implémentation.

**Portes concernées** : `porte-flux`, `porte-pont`, `porte-coupe` (régime 1 %), `porte-echange-experts`
(invariant du routage), et `cargo test placement`. Aucune porte ne mesure **le placement des experts**
aujourd'hui : c'est le trou que la prochaine expérience comble, et la raison pour laquelle la
règle peut être fausse sans qu'aucune porte ne rougisse.

## 5. Ce que cette reconnaissance n'a pas fait

- **aucun fichier du moteur modifié**, **aucun commit**, `docs/pilotage/en-cours.md`,
  `docs/pilotage/roadmap.md` et `AGENTS.md` **non touchés** ;
- pas de mesure de **VRAM** sur les experts : le cache Q4_K n'est pas câblé (garde MXFP4),
  et le noyau GPU Q4_K existe mais n'est pas branché — c'est **le** travail de code que la
  prochaine expérience doit précéder ou suivre ;
- les temps sont pris **machine chargée** (13,7 → 31,4) : les rejouer au repos avant de les citer ;
- `rapport-etat-a.md` § 1.5 citait `modeles/gguf/…` : le fichier est sous `$HOME/IA/modeles/`
  (correction déjà faite par `rapport-coordination-a.md`, reprise ici).
