# Session 9f4f7b6d — Tu travailles dans /home/stephane/Data13

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `9f4f7b6d-c5aa-4269-b785-a0f444424470` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 10:17 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 49 |
| Appels d'outils | 61 |
| Fichiers touchés | 2 |
| Commandes | 32 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée. La reconnaissance `reports/rapport-a2.6-reconnaissance.md` a montré que `drave-core/src/placement.rs` n'a **aucune entrée `Precision` pour la tête** en Q8_0/Q6_K (la table a f32, int8 tardif, int4 tardif, « tête 4 bits +10 % », int4 global +364 %), alors qu'une mesure de la reconnaissance donne … [2033 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée. La reconnaissan … [2313 caractères tronqués]

*61 appels d'outils.* Actions notables :

- read
- bash — Vue du dépôt et état git
- bash — Lancer cargo test placement (état de base)
- bash — Lister reports et taille du rapport de reconnaissance
- bash — Trouver le Cargo.toml du crate
- bash — cargo test placement état de base
- bash — Chercher les usages de PRECISIONS et choisir_avec_perte
- bash — cargo test complet de référence
- bash — Repérer les codes/types Q8_0 et Q6_K
- bash — Lire le site tête de model.rs en lecture seule
- job_output
- bash — Vérifier deny/allow et constantes F32/F16
- bash — Vérifier HEAD et propreté du crate
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs`
- … et 40 autres

**Synthèse produite :**

⏵ Tâche terminée : entrées tête Q8_0/Q6_K ajoutées et testées

\## Diff (résumé)

**`drave-core/src/placement.rs`** — seul fichier de code modifié : **+117 / −0** lignes (253 → 370), aucun commit.

| élément | lignes | contenu |
|---|---:|---|
| `TETE_Q8_0` | 172-176 | `1,0625` o/valeur (34 o / bloc de 32), **perte 0,0** |
| `TETE_Q6_K` | 182-186 | `0,8203125` o/valeur (210 o / bloc de 256), **perte 0,0** |
| `precision_tete(type_ggml)` | 188-202 | `GGML_F32/GGML_Q8_0/GGML_Q6_K` → `Precision`, sinon `None` |
| `choisir_tete(...)` | 204-226 | place la tête **dans son format** ; `perte_max` négatif ⇒ `None` |
| test `la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle` | 302-349 | le test demandé |

**Choix assumé** : les entrées sont **hors de `PRECISIONS`**, car `choisir_avec_perte` prend le moins cher sous budget — une entrée à perte 0 y gagnerait à budget nul contre f32 (et dès 1 % contre int8), cassant 2 des 8 tests. La table générique, ses 5 constantes et `choisir_avec_perte` sont inchangés au caractère près. `perte_ppl: 0.0` signifie **aucune perte due au placement** (même format du fichier), pas « Q8_0 = f32 ».

\## Comptes

| commande | avant | après |
|---|---:|---:|
| `cargo test placement` | 8/8 | **9/9**, 0 échec |
| `cargo test` (crate) | 139/139 | **140/140**, 0 échec |

**Contrôle de retrait** : sans la ligne `GGML_Q8_0 => Some(TETE_Q8_0)`, `cargo test placement` donne **8 passed, 1 failed** (exit 101, panique sur l'`unwrap`) ; entrée remise → 9/9. `model.rs` et `main.rs` sont intacts : aucun câblage, aucun changement de défaut.

\## Rapport

**`reports/rapport-a2.6-tete-q8.md`** (268 lignes) : la mesure de la reconnaissance (56,7642 = 56,7642 ; 7,43 → 1,80 ms/jeton ; contrôle `DRAVE_GPU=0`), le diff et ses lignes, le test, les comptes, et ce qui pourrait le rendre faux — **machine chargée** (13,7 → 31,4, à rejouer au repos), égalité de PPL imprimée à 4 décimales, **Q6_K jamais mesuré** (0,0 par construction, signalé comme à rejouer), octets nominaux/alignement des blocs, repli NVMe silencieux préexistant.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs` | 0 | 7 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md` | 1 | 11 |

### Commandes exécutées (échantillon)

- **T1** Vue du dépôt et état git
- **T1** Lancer cargo test placement (état de base)
- **T1** Lister reports et taille du rapport de reconnaissance
- **T1** Trouver le Cargo.toml du crate
- **T1** cargo test placement état de base
- **T1** Chercher les usages de PRECISIONS et choisir_avec_perte
- **T1** cargo test complet de référence
- **T1** Repérer les codes/types Q8_0 et Q6_K
- **T1** Lire le site tête de model.rs en lecture seule
- **T1** Vérifier deny/allow et constantes F32/F16
- **T1** Vérifier HEAD et propreté du crate
- **T1** cargo test placement après ajout
- **T1** Avertissements liés à placement.rs en build normal
- **T1** Voir le diff courant de placement.rs
- **T1** Prouver l'échec du test sans l'entrée Q8_0
- **T1** Retour au vert et contrôle du diff
- **T1** cargo test complet après ajout
- **T1** Relever les numéros de lignes du bloc ajouté
- **T1** Chercher des avertissements sur les lignes 160-225
- **T1** Date, HEAD, état git et numstat
- **T1** Vérifier existence et style d'un rapport voisin
- **T1** Lignes exactes de _tete_tient et des constantes ggml
- **T1** Historique de placement.rs depuis la mesure
- **T1** Tests placement et crate complet (final)
- **T1** Contrôle des fichiers modifiés et des fichiers interdits
- **T1** Numéros de lignes après la retouche de doc
- **T1** Lister les chiffres à actualiser dans le rapport
- **T1** Extraire le test final pour comparaison
- **T1** Vérifier qu'aucun chiffre périmé ne reste
- **T1** Confirmer le nom DRAVE_PERTE_MAX
- **T1** Comptes finaux des tests
- **T1** État final des fichiers

## 4. Mesures et résultats marquants

- **T1** `src/model.rs:4842:        // rapide que le chemin scalaire Q6_K, qui coûtait 42 % du temps par`
- **T1** `src/model.rs:9240:    /// (3,4 ms pour 151 936 × 896 en Q8_0), payée une fois.`
- **T1** `// rapide que le chemin scalaire Q6_K, qui coûtait 42 % du temps par`
- **T1** `// de 23 à 159 ms. Le noyau lit une ligne par fil, donc des adresses`
- **T1** `// rentable : l'ancien lisait une ligne par fil (23 → 159 ms mesurés).`
- **T1** `// mesurées, la mesure du 24/10 valide cette ligne (×1,93 au prefill).`
- **T1** `// reste. Mesuré : la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM,`
- **T1** `// et un cache de 25 % de l'empreinte sert 80 % des appels.`
- **T1** `// cette machine (110 Mo pour le 0,5 B) — et la tête s'y place sans drapeau.`
- **T1** `// coûte +10 % de perplexité (30,7660 → 33,8230). La règle de PLACE ne dit rien`
- **T1** `+// (56,7642 = 56,7642) et passe de 7,43 à 1,80 ms/jeton. Ce n'est pas un choix de`
- **T1** `+/// garde alors son défaut. Les formats 4 bits restent `TETE_4BIT` (+10 % mesurés).`
- **T1** `/// **+2,28 %** sur les premières, **+0,03 %** sur les dernières. La frontière mesurée`
- **T1** `+        // PPL qu'en RAM (56,7642 = 56,7642), 7,43 → 1,80 ms/jeton. La règle ne doit`
- **T1** `+        // Contrôle négatif : un type que la règle ne connaît pas (Q4_K, +10 %)`
- **T1** `// 24 couches : l'int8 passe sur les 12-23 (+0,03 %), pas sur les 0-11 (+2,28 %).`
- **T1** `> **accélère le calcul** : **24,0 → 30,5 tok/s** (+27 %) dès le lot 2, et le temps mural passe de`
- **T1** `> soit **−0,006 %**.`
- **T1** `**Le lot accélère le calcul.** Dès le lot 2, le préremplissage passe de 24,0 à 30,5 tok/s (+27 %)`
- **T1** `b22b7097 A8.3 — LA REGLE PLACE ET PERTE EST BRANCHEE : placement::kv_precision choisit la precision du KV par couche selon le budget DRAVE_PERTE_MAX (defaut 1 %) — l'int8 si sa perte mesuree tient (+2`
- **T1** `976d55e4 A7.2 + A8.2 — LE RELAIS A CHIFFRE EGAL, ET LA PERTE ENTRE DANS LA REGLE. A7.2 etabli : porte-topologie (92 s, 42.5477) — une couche executee ailleurs rend la meme sortie, le flux coute 1 608 `
- **T1** `/// défaut. La **requantification** 4 bits, elle, reste `TETE_4BIT` (+10 % mesurés).`
- **T1** `// PPL qu'en RAM (56,7642 = 56,7642), 7,43 → 1,80 ms/jeton. La règle ne doit`
- **T1** `4709:        // premières couches, +0,03 % sur les dernières (A5.3) — le budget `DRAVE_PERTE_MAX``

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : test placement::tests::la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle ... FAILED failures: ---- placement::tests::la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle stdout ---- thread 'placement::test
- **T1** : (no output) [exit code: 1]

