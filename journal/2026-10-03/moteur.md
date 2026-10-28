# 2026-10-03 — Moteur : chargement, calcul, listes, quantification

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (21)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 00:01 | `7f60f39c` | Sprint 18 : clôture (28 min) — deux noyaux AVX2 bit-exacts (Q2_K et IQ1_M), portes toutes vertes | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 01:16 | `20de26e3` | Bloc 19 : première passe V4.1 de 1 024 jetons (1 023 notés, PPL 1 287 700,8239, 60,6 min, aucun incident) — et le profil par profondeur n'avait aucun drapeau | `main.rs`, `README.md`, `MANIFEST.md` (+3) |
| 01:17 | `b37088ad` | Sprint 19 : clôture (76 min) — la passe longue est passée, le profil par profondeur est réparé, et 63 tests verts | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 01:18 | `be5d2a11` | Docs : le drapeau --ppl-profil n'est plus « inexistant » — l'avertissement de docs/vision.md, le glossaire et le rapport d'audit des drapeaux ignorés sont mis à jour | `glossaire.md`, `vision.md`, `MANIFEST.md` (+5) |
| 03:24 | `14c52ae7` | Localisation V4.1 : huit hypothèses éliminées par ablation, et le défaut est cerné au chemin partagé tel que V4.1 l'instancie | `main.rs`, `model.rs`, `README.md` (+5) |
| 03:32 | `98c3401b` | Localisation V4.1, suite : l'embarquement est exact (0,000e+00), le biais de routeur du texte est le bon, et la règle du retard est CONFORME à la source publiée | `main.rs`, `model.rs`, `README.md` (+4) |
| 03:47 | `3f096a17` | Défaut silencieux corrigé : --abits au-delà de 16 saturait (et parfois enroulait) les activations i16 — facteur 256 muet | `main.rs`, `model.rs`, `README.md` (+4) |
| 03:49 | `08fbf237` | Deux vides neufs pour rendre le chemin des experts vérifiable : ffn_hn (entrée normée du MoE, vérifiée en numpy à 1e-7) et moe_down (somme des experts routés) | `model.rs`, `README.md`, `MANIFEST.md` (+3) |
| 06:50 | `0553b8d0` | DRAVE_SIMD_DOT : le produit scalaire des experts vectorisé — ×2,06 sur la passe, et l'écart qu'il introduit est MESURÉ | `REPRISE.md`, `plan-deepseek41-complet.md`, `main.rs` (+6) |
| 08:17 | `1d459614` | GPU : le tandem NVLink est au repos sur la charge principale, et les chiffres disent pourquoi | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 09:14 | `d13e3532` | Granularité des listes : elle ROUTE, elle ne compresse pas — mesuré sur les activations réelles de V4-Flash | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 11:05 | `984663db` | KDA (delta-net de Kimi-K3) : la récurrence implémentée et vérifiée contre une référence NumPy | `model.rs`, `README.md`, `MANIFEST.md` (+2) |
| 12:01 | `6b7b7fac` | Kimi-K3 : l'inventaire des tenseurs, vérifié sur le fichier (49 couches vues, cadence KDA/MLA confirmée) | `kimi_k3.rs`, `main.rs`, `README.md` (+3) |
| 12:28 | `1cdc767c` | K3 : les dimensions des quatre types de couches sont CONFORMES au fichier (0 dense, 1 MoE+KDA, 3 MoE+MLA, 4 KDA) | `kimi_k3.rs`, `main.rs`, `README.md` (+3) |
| 12:29 | `c29cbc2b` | K3 : la couche 0 vide ses sorties au format du moteur — la comparaison tenseur par tenseur n'attend plus que la référence | `verification-kimi-k3.md`, `main.rs`, `README.md` (+3) |
| 12:44 | `f0d980b8` | K3 : le MoE latent fonctionne — et 25,7 s/jeton sont devenus 1,36 s (×18,9) sans changer un chiffre | `kimi_k3.rs`, `main.rs`, `README.md` (+3) |
| 12:58 | `b0c14b95` | K3 : les quatre premières couches COMPOSÉES (0 dense, 1-2 MoE, 3 MLA) — la chaîne vérifiée, pas seulement les pièces | `kimi_k3.rs`, `main.rs`, `README.md` (+3) |
| 14:27 | `3bf4ef3a` | Bloc 31 : le regroupement par experts vaut x1,58 — et Kimi-K3 est arrivé au complet | `plan-kimi-k3.md`, `main.rs`, `model.rs` (+8) |
| 15:39 | `058ea00f` | Tuile du GEMM par lots : hypothèse avancée, mesurée, RÉFUTÉE | `engine.rs`, `main.rs`, `README.md` (+4) |
| 18:05 | `053426c1` | K3 : la cadence des couches a une EXCEPTION, et le moteur ne l'a pas codée en dur | `architecture-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 18:16 | `1462acad` | K3 : composer 13 couches, le premier essai qui franchit une BANQUE | `main.rs`, `README.md`, `MANIFEST.md` (+2) |

## Chiffres du jour

`13 couches` · `×18,9` · `25,7 s` · `1,36 s` · `49 couches` · `×2,06` · `1024 jetons` · `700,8239`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

## Mesures et rapports touchés

- [reports/rapport-drapeaux-ignores.md](../../reports/rapport-drapeaux-ignores.md)
- [reports/rapport-gpu-tandem-nvlink.md](../../reports/rapport-gpu-tandem-nvlink.md)
- [reports/rapport-granularite-flux.md](../../reports/rapport-granularite-flux.md)
- [reports/rapport-prefill-par-experts.md](../../reports/rapport-prefill-par-experts.md)

<!-- notes -->

<!-- /notes -->
