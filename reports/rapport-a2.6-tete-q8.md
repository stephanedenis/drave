# A2.6 — la tête Q8_0/Q6_K entre dans la règle, à perte nulle

> **Verdict.** `placement.rs` porte désormais la **tête du fichier** comme précision :
> `TETE_Q8_0` (**1,0625** octet par valeur, 34 octets par bloc de 32) et `TETE_Q6_K`
> (**0,8203** octet par valeur, 210 octets par super-bloc de 256), toutes deux à
> **perte 0,0**. Ce n'est **pas** une requantification : la mesure de la reconnaissance
> (18/11, § 3.4) pose la tête **Q8_0 du fichier** en VRAM sans bouger la perplexité
> (**56,7642 = 56,7642**) et en divisant son temps par **4,1** (7,43 → **1,80 ms/jeton**).
> Le diff est **+117 / −0** lignes ; **aucun câblage** : `model.rs` n'est pas touché, le
> défaut ne bouge pas, le comportement à l'exécution est identique (les points d'entrée
> neufs ne sont appelés que par le test).
>
> **Date** : 2026-11-18. **Ligne de roadmap** : A2.6 (ordonnanceur : la tête).
> **HEAD** : `8bec3cc8`. **Nature** : implémentation **testée**, **sans commit**.
> **Fichiers écrits** : `drave-core/src/placement.rs` (seule modification de code) et ce
> rapport. `docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`, `AGENTS.md`,
> `model.rs`, `main.rs` : **non touchés**.

## 1. La mesure qui justifie l'entrée

Reprise de [`rapport-a2.6-reconnaissance.md`](rapport-a2.6-reconnaissance.md) § 3.4
(mesure du 18/11, **Qwen2.5-0.5B-Q8_0.gguf**, `--ppl ids_0.5B_wt2_8192.txt --ctx 512
--limit 32 --threads 8`, 2 × Quadro RTX 5000) :

| chemin | PPL | tête (ms/jeton) | tok/s |
|---|---:|---:|---:|
| CPU (défaut) | 56,7642 | 7,43 | 24,6 |
| **VRAM (`DRAVE_GPU_TETE=1`, tête Q8_0 du fichier)** | **56,7642** | **1,80** | **28,4** |
| contrôle `DRAVE_GPU=0` | 56,7642 | 7,75 | 24,0 |
| `--q4-tout` (4 bits partout) | 79,9488 (+40,8 %) | 6,50 | 42,4 |

Ce que cette table prouve **exactement** : changer le **support** de la tête Q8_0 ne
change pas la perplexité (même précision lue dans le fichier, aucune requantification) ;
ce que coûte la tête est donc bien un **placement**, pas une précision. C'est ce que
l'entrée encode par `perte_ppl: 0.0` : **aucune perte supplémentaire due au placement** —
et non « Q8_0 vaut f32 en qualité ». La distinction est importante : la mesure compare
Q8_0 en RAM à Q8_0 en VRAM, pas Q8_0 à f32.

Le contrôle négatif de la mesure est le troisième chemin : sans GPU (`DRAVE_GPU=0`), la
tête reste à 7,75 ms et la PPL ne bouge pas — le gain vient du support, pas d'un artefact
de mesure.

**Aucun commit n'a touché `placement.rs` entre `bb57604c` (HEAD de la mesure) et
`8bec3cc8`** (`git log bb57604c..HEAD -- drave-core/src/placement.rs` : vide) : la règle
sur laquelle la mesure a été faite est celle de ce diff.

## 2. Le diff

`git diff --numstat drave-core/src/placement.rs` → **117 ajouts, 0 suppression**
(fichier de 253 → **370** lignes), uniquement des ajouts.

| élément | lignes | rôle |
|---|---:|---|
| bloc tête (commentaire de section + tout ce qui suit) | **160-226** | le format du fichier, pas une requantification |
| `TETE_Q8_0` | 172-176 | `nom: "tête Q8_0"`, `octets_par_valeur: 34.0/32.0`, `perte_ppl: 0.0` |
| `TETE_Q6_K` | 182-186 | `nom: "tête Q6_K"`, `octets_par_valeur: 210.0/256.0`, `perte_ppl: 0.0` |
| `precision_tete(type_ggml)` | 188-202 | type ggml → `Precision` ; `None` sinon |
| `choisir_tete(...)` | 204-226 | place la tête **dans son format**, sous budget de perte |
| test `la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle` | **302-349** | le test demandé |

### 2.1 L'API ajoutée

```rust
pub const TETE_Q8_0: Precision = Precision {
    nom: "tête Q8_0", octets_par_valeur: 34.0 / 32.0, perte_ppl: 0.0,
};
pub const TETE_Q6_K: Precision = Precision {
    nom: "tête Q6_K", octets_par_valeur: 210.0 / 256.0, perte_ppl: 0.0,
};

pub fn precision_tete(type_ggml: u32) -> Option<Precision>;   // F32 / Q8_0 / Q6_K, sinon None

pub fn choisir_tete(
    type_ggml: u32,          // le type du tenseur dans le fichier
    nb_valeurs: u64,         // vocab × caché (ou le vrai compte du tenseur)
    libre_vram: u64,
    libre_ram: u64,
    perte_max: f64,          // 0.0 = exiger une tête qui ne coûte rien à la PPL
) -> Option<(Support, Precision)>;
```

- **Le type ggml est celui du fichier**, pas un numéro inventé : `GGML_F32 = 0`,
  `GGML_Q8_0 = 8`, `GGML_Q6_K = 14` (`drave-core/src/gguf.rs:573,630,589`). Un type
  **sans entrée** rend `None` — la règle ne devine ni les octets ni la perte
  (Q4_K/Q5_K/F16 ne sont pas couverts ; la **requantification** 4 bits reste
  `TETE_4BIT`, +10 %).
- **Les octets** : Q8_0 = 34 octets par bloc de 32 poids (échelle f16 + 32 quants) =
  **1,0625** o/valeur ; Q6_K = 210 octets par super-bloc de 256 (128 + 64 + 16 quants,
  2 d'échelle, cf. `gguf.rs` `TAILLE_Q6K = 210`) = **0,8203125** o/valeur. Les deux
  valeurs sont des fractions exactes en binaire (`17/16`, `105/128`), donc les
  assertions d'égalité du test sont sûres.
- **Pas de champ `bits` ajouté** : `Precision` porte `octets_par_valeur`, et c'est la
  seule grandeur que la règle de coût utilise (`cout`). Ajouter un `bits` décoratif
  obligerait à réécrire les **5** constantes existantes pour zéro décision ; les
  largeurs (8 bits + échelle de 2 o par 32 ; 6 bits + 18 o d'échelles par 256) sont dans
  les commentaires de doc, et les octets exacts sont dans la constante.
- **Le coût de la tête** : elle est lue **en entier une fois par jeton**, un seul
  lecteur ; `octets_par_jeton == octets_total == nb_valeurs × octets_par_valeur`. C'est
  le modèle qui explique 7,43 → 1,80 ms. (Limite : les octets sont **nominaux** ; si la
  ligne du tenseur n'est pas un multiple du bloc, le câblage devra passer le nombre de
  blocs réel — 32 pour Q8_0, 256 pour Q6_K.)

### 2.2 Pourquoi les entrées ne sont **pas** dans `PRECISIONS`

`choisir_avec_perte` parcourt `PRECISIONS` et prend le **moins cher** sous le budget.
Une entrée à perte 0,0 de 0,82-1,06 o/valeur gagnerait **à budget nul** contre le f32, et
dès 1 % contre l'int8 : deux des huit tests existants tomberaient
(`un_budget_nul_interdit_toute_quantification` attend `"f32"` ;
`la_perte_decide_aussi` attend `"int8 tardif"` à 1 %). La consigne « ne pas casser les
8 tests » et une entrée à perte nulle dans la table générique sont donc incompatibles —
et c'est heureux : les deux tables ne disent pas la même chose.

| table | ce qu'elle décrit | choix |
|---|---|---|
| `PRECISIONS` (inchangée, 5 entrées) | les **requantifications** d'un opérateur f32, avec leur perte mesurée | le moins d'octets sous budget |
| `TETE_Q8_0` / `TETE_Q6_K` (neuves) | le **format déjà écrit dans le fichier** | le support, à format donné |

`PRECISIONS`, les 5 constantes existantes et `choisir_avec_perte` sont **inchangés** au
caractère près : les 8 tests d'origine passent sans modification.

Les deux fonctions neuves portent `#[allow(dead_code)]` (commentaire : « pas encore
branché ») : c'est voulu, la tâche interdit le câblage. Sans l'attribut, elles
ajouteraient deux avertissements `never used` — le reste de la couche `Precision` est
déjà dans ce cas en build normal (`PRECISIONS`, `choisir_avec_perte` sont `never used`
hors tests), donc le build ne change pas de statut.

## 3. Le test

`placement.rs:302-349`, un seul test :

```rust
#[test]
fn la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle() {
    // La mesure de la reconnaissance (18/11, § 3.4) : tête Q8_0 en VRAM, même
    // PPL qu'en RAM (56,7642 = 56,7642), 7,43 → 1,80 ms/jeton. La règle ne doit
    // donc pas déplacer la tête Q8_0 : elle la pose où le f32 se poserait.
    let n = 151_936u64 * 896;               // la tête d'un 0,5 B (vocab × caché)
    let octets_f32 = n * 4;

    // La référence : le f32 à budget nul, par la règle générique.
    let (sup_f32, p_f32) = choisir_avec_perte(octets_f32, octets_f32, 16 << 30, 64 << 30, 0.0)
        .unwrap();
    assert_eq!(p_f32, F32);

    // En f32, le nouveau chemin rend EXACTEMENT la réponse du chemin générique.
    assert_eq!(
        choisir_tete(crate::gguf::GGML_F32, n, 16 << 30, 64 << 30, 0.0),
        choisir_avec_perte(octets_f32, octets_f32, 16 << 30, 64 << 30, 0.0)
    );

    // La tête Q8_0 : la même place que la référence, perte nulle, bon format.
    let (sup_q8, p_q8) =
        choisir_tete(crate::gguf::GGML_Q8_0, n, 16 << 30, 64 << 30, 0.0).unwrap();
    assert_eq!(p_q8, TETE_Q8_0);
    assert_eq!(p_q8.perte_ppl, 0.0);
    assert_eq!(sup_q8, sup_f32);
    assert_eq!(p_q8.octets_par_valeur, 34.0 / 32.0);

    // Q6_K : encore moins d'octets, même perte déclarée.
    assert_eq!(TETE_Q6_K.octets_par_valeur, 210.0 / 256.0);
    assert!(TETE_Q6_K.octets_par_valeur < TETE_Q8_0.octets_par_valeur);

    // Un budget négatif refuse la tête, même sans perte.
    assert_eq!(
        choisir_tete(crate::gguf::GGML_Q8_0, n, 16 << 30, 64 << 30, -0.1),
        None
    );

    // Contrôle négatif : un type sans entrée (Q4_K) rend None — la règle
    // ne devine pas les octets d'un format qu'elle ne porte pas.
    assert_eq!(
        choisir_tete(crate::gguf::GGML_Q4_K, n, 16 << 30, 64 << 30, 0.0),
        None
    );
}
```

Ce qu'il vérifie, dans l'ordre :

1. **référence** : à budget 0, la règle générique choisit `F32` (les 8 tests d'origine
   décrivent déjà ce contrat) ; le support est la VRAM pour une tête de 545 Mo ;
2. **le nouveau chemin ne réinvente pas le placement** : appelé avec `GGML_F32`, il rend
   **exactement** la même paire `(Support, Precision)` que `choisir_avec_perte` ;
3. **la tête Q8_0** est placée **au même support** que cette référence (VRAM), avec
   `perte_ppl == 0.0` et les bons octets (34/32) ;
4. **une perte négative la refuse** (`-0.1` → `None`) : le budget est un plafond, pas un
   plancher ;
5. **contrôle négatif** : un format **sans entrée** (`GGML_Q4_K`) → `None` : la règle
   ne devine pas les octets d'un format qu'elle ne porte pas.

**Le test échoue bien si l'entrée est retirée.** Vérifié en retirant temporairement la
ligne `GGML_Q8_0 => Some(TETE_Q8_0),` de `precision_tete`, puis en la remettant :

| état | `cargo test placement` |
|---|---|
| entrée retirée | **8 passed, 1 failed** (`test result: FAILED`, code 101) — panique sur le `.unwrap()` de `choisir_tete(GGML_Q8_0, …)` |
| entrée remise | **9 passed, 0 failed** |

Les 8 tests d'origine ne sont pas modifiés (diff : 0 suppression) et passent dans les
deux états : c'est l'entrée neuve, et elle seule, que le test surveille.

## 4. Ce qui pourrait rendre le chiffre faux

- **La machine était chargée** : charge **13,7 → 31,4** pendant les mesures de la
  reconnaissance (d'autres sessions lisaient un modèle lourd). Les temps absolus
  peuvent bouger de **±20 %** ; l'égalité de PPL et l'ordre des supports, non. **À
  rejouer machine au repos** avant de citer 1,80 ms comme un chiffre de référence.
- **L'égalité de PPL n'est imprimée qu'à 4 décimales** (56,7642 = 56,7642) : ce n'est pas
  une preuve d'égalité bit à bit. L'argument d'exactitude du noyau GPU (2e-7 sur les
  logits) vient d'un **autre** rapport et d'un autre modèle — il ne se transporte pas
  silencieusement ici.
- **Q6_K n'a jamais été mesuré.** La seule tête mesurée est Q8_0. `perte_ppl: 0.0` pour
  Q6_K est vrai **par construction** (le format est déjà dans le fichier : le placer ne
  le requantifie pas), mais aucun run ne l'a vérifié sur la tête. Q6_K est à **rejouer**
  avant d'être cité comme mesuré ; c'est écrit dans sa doc.
- **Une tête, un modèle, 31 jetons notés** (`--limit 32`, 0,5 B) : la mesure ne dit rien
  des autres architectures ni des têtes non liées.
- **Les formats non couverts** : Q4_K, Q5_K, F16 rendent `None` — la règle ne les place
  pas (voulu : elle ne porte que les entrées du fichier qu'elle documente). Une tête
  Q4_K reste donc sur le chemin d'avant ; le `--q4-tout` (+40,8 %) n'est pas devenu
  plaçable.
- **Le modèle de coût suppose une lecture entière, un lecteur** : un noyau qui
  n'échantillonnerait que des lignes candidates paierait moins que `nb_valeurs ×
  octets_par_valeur`. Les 7,43 → 1,80 ms sont compatibles avec la lecture entière, ils
  ne la prouvent pas pour tous les chemins d'échantillonnage.
- **Les octets sont nominaux** : le calcul `nb_valeurs × octets_par_valeur` ignore le
  remplissage de bloc si la ligne n'est pas alignée (32 pour Q8_0, 256 pour Q6_K). Sur
  la tête mesurée (151 936 × 896) la division est exacte, mais le câblage devra passer
  le nombre de blocs réel.
- **`choisir` retombe silencieusement sur le NVMe** si rien ne tient (comportement
  existant, non touché) : « placée » peut vouloir dire « streaming disque », pas
  « résidente ». Le refus nommé reste à faire (A2.6, point 2 de la reconnaissance).
- **La mesure ne dit pas que Q8_0 vaut f32** : elle dit que **déplacer** la tête Q8_0 ne
  coûte rien à la PPL du fichier. C'est la seule lecture autorisée de `perte_ppl: 0.0`.

## 5. Comptes et commandes

```bash
cd drave-core
cargo test placement     # 9 passed; 0 failed; 0 ignored (131 filtrés)
cargo test               # 140 passed; 0 failed; 0 ignored (avant : 139/139)
```

| mesure | avant | après |
|---|---:|---:|
| `cargo test placement` | 8 / 8 | **9 / 9** |
| `cargo test` (crate entier) | 139 / 139 | **140 / 140** |
| lignes de `placement.rs` | 253 | **370** |
| diff | — | **+117 / −0**, 1 fichier |

- `git status` : `drave-core/src/placement.rs` modifié, ce rapport ajouté ; **aucun
  commit**, aucun autre fichier de code touché (les modifications `journal/` visibles
  dans `git status` viennent d'autres sessions, pas de ce diff).
- Build : **pas de nouvel avertissement** sur les lignes 160-226 (vérifié par
  `cargo build` après `touch`), les deux fonctions étant `#[allow(dead_code)]` en
  attendant le câblage.

## 6. Ce que la tâche suivante doit faire (câblage, hors de ce diff)

1. **Brancher** `choisir_tete` à `model.rs:4988`, là où `_tete_tient` est aujourd'hui un
   calcul jeté : passer le **type ggml** de la tête (`tete.ttype`) et
   `cfg.vocab × cfg.hidden` (ou le compte de blocs réel), sous un garde-fou **opt-in**
   (le `DRAVE_PERTE_MAX` existant, par exemple), pour que le **défaut ne bouge pas**
   (A8.3b). Imprimer le support et la précision retenus, et le refus le cas échéant.
2. **Rejouer la mesure** de la tête Q8_0 machine au repos, et **mesurer Q6_K** (tête
   liée d'un Qwen en Q4_K_M, par exemple) avant de citer 0,0 pour Q6_K.
3. Si le +10 % de la tête 4 bits doit être rejoué isolément, ajouter un `--q4-tete` :
   aujourd'hui `--q4-tout` est confondu (tout le modèle en 4 bits, +40,8 %).
