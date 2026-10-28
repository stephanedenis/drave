# 2026-10-03 — Portes et vérifications

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (24)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 03:57 | `50db1505` | Sprint 21 : portes toutes vertes après les changements du bloc (64 tests, V4-Flash 8430,4966 inchangée) | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:14 | `e79cb2dc` | Plan P7 : la porte de correction est IMPOSSIBLE en l'état et c'est nommé — llama.cpp refuse l'architecture deepseek41 ; ce qui est vérifiable sans référence exécutable l'est (tableau des douze vérifications) | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+2) |
| 04:19 | `314ff84d` | Porte Drave de P6, point 1 CORRIGÉ : l'outil d'analyse lit les trois versions du format DRVF, et la porte est branchée | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+4) |
| 04:21 | `6faea8f2` | Porte Drave de P6, point 2 : le rejeu est DÉFINI et VÉRIFIÉ — 0 liste manquante, écart ≤ 1e-5, et la cause de l'écart est mesurée | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+3) |
| 04:39 | `38fb6782` | Porte de correction P6 serrée : 63 positions, corrélation 0,9852, top-1 88,9 %, PPL à 6,4 % | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+2) |
| 04:43 | `e57cd157` | Sprint 22 : la composition de V4.1 est vérifiée pièce par pièce, et les deux portes de P6, exécutées, étaient fausses deux fois sur quatre | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 04:48 | `02ff0bac` | La porte de correction devient un OUTIL exécutable, branché dans portes.sh (Qwen, 71 positions) | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 05:03 | `5b121781` | Glossaire : la porte de correction a maintenant des critères mesurés, et le rejeu une définition vérifiée | `glossaire.md`, `README.md`, `MANIFEST.md` (+2) |
| 05:38 | `1b52c5b4` | Sprint 23 : la porte de correction serrée (63 positions, 6,4 % au lieu de 25 %), outillée (verdict + code retour), et le coût du contexte long mesuré | `REPRISE.md`, `README.md`, `MANIFEST.md` (+3) |
| 09:15 | `dba369fe` | Plan P6 : porte de correction TENUE à ctx 512 (511 positions, top-1 93,0 %, +4,3 % de PPL) et le coût par jeton ne croît presque pas avec le contexte (2,58 s/jeton contre 2,50 à ctx 64) | `plan-deepseek41-complet.md`, `vision.md`, `README.md` (+3) |
| 09:28 | `8bce1b40` | Sprint 26 : porte de correction TENUE à ctx 512, coût par jeton quasi constant, granularité qui route — portes toutes vertes | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:30 | `28d3c9ff` | REPRISE : état du 03/10 (porte à ctx 512, coût plat, SIMD corrigé, granularité) | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 09:43 | `c9b77544` | Porte Drave de P1 TENUE : mesurée, et elle révèle une structure — les 16 connexions de V4-Flash sont une PERMUTATION | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+4) |
| 09:45 | `30ee8596` | Audit : les deux portes, phase par phase (P0 à P9) — ce qui est tenu, ce qui est impossible et nommé, ce qui reste à la demande | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:48 | `4973c78d` | Plan : renvoi vers l'audit des deux portes, phase par phase | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+2) |
| 10:13 | `08ced099` | Retrait de V4-Flash : copie NVMe supprimée, porte hc repointée sur V4.1 (testée), section 6bis marquée ARCHIVÉE dans portes.sh | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:24 | `ce409dd7` | Porte de correction à ctx 1024 (1 023 positions) : accord MEILLEUR (moyenne 0,9914, top-1 93,5 %, PPL +1,7 %), mais elle a d'abord échoué sur une position où la référence est certaine | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+3) |
| 10:25 | `bd9b9363` | Sprint 27 : porte P1 fermée (et elle révèle une permutation), portes auditées P0-P9, porte à ctx 1024 tenue sous critère révisé, bascule vers Kimi-K3 | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 11:01 | `f536b53c` | Spec Kimi-K3 : le KDA, sa porte bornée à -5, ses trois chemins de référence et les tenseurs qui serviront de points de comparaison | `architecture-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 11:08 | `b97f929b` | KDA : porte bornée et convolution courte implémentées et testées — le test a attrapé une inversion de disposition d'état | `architecture-kimi-k3.md`, `model.rs`, `README.md` (+3) |
| 12:51 | `dd4f0572` | K3 : la couche MLA calcule (couches 3, 7, 11…) — absorption par tête, nope sans rotation, porte sigmoïde pleine largeur | `kimi_k3.rs`, `main.rs`, `README.md` (+3) |
| 16:04 | `f2116f04` | Bloc 31 : la porte gpt-oss, son motif réel, et l'arbitrage assumé | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 20:06 | `36f1243a` | ref_logits : REF_SANS_REPACK, la porte qui rend la référence K3 exécutable ici | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 22:35 | `75c72364` | K3 : le premier jalon de vérification est NÉGATIF — et il désigne l'état, pas la forme | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+3) |

## Chiffres du jour

`93,5 %` · `+1,7 %` · `0,9914` · `93,0 %` · `+4,3 %` · `2,58 s` · `6,4 %` · `25 %` · `88,9 %` · `0,9852` · `8430,4966`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

## Mesures et rapports touchés

- [reports/rapport-hc-permutation.md](../../reports/rapport-hc-permutation.md)
- [reports/rapport-portes-p0-p9.md](../../reports/rapport-portes-p0-p9.md)

<!-- notes -->

<!-- /notes -->
