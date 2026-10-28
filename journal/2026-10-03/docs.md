# 2026-10-03 — Documentation, état, conventions

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (27)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:20 | `e8a351e5` | Cohérence : le rapport d'audit des docs est daté (quatre de ses trouvailles sont corrigées depuis) et le mode du champ n est écrit pour les cinq modes | `format-flux.md`, `README.md`, `MANIFEST.md` (+3) |
| 02:54 | `b5e7d9c8` | ⚠️ V4.1 ne prédit pas : top-1 0/31, NLL 11,657 nats (uniforme 11,770) — V4-Flash, lui, est juste (1,875 contre 1,844 pour llama.cpp) | `REPRISE.md`, `plan-deepseek41-complet.md`, `README.md` (+6) |
| 02:56 | `9250879b` | Sprint 20 : clôture (103 min) — la passe longue a livré son verdict : V4.1 ne prédit pas, V4-Flash est juste | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 03:34 | `05c2416d` | Journal : index de session à jour | `README.md`, `MANIFEST.md`, `digest.md` (+1) |
| 03:34 | `3252ec7a` | Sprint 21 : clôture (35 min) — douze hypothèses éliminées, quatre pièces vérifiées, le défaut cerné au chemin des experts | `README.md`, `MANIFEST.md`, `digest.md` (+3) |
| 04:52 | `fce7f490` | compare_logits.py : un diagnostic par TRANCHES, pour distinguer une erreur de position d'une erreur de tête | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+3) |
| 05:38 | `a252e71c` | Plan P6 : le coût du contexte long est mesuré (60 s/jeton à ctx 1024), et --dense est inerte pour V4-Flash | `plan-deepseek41-complet.md`, `README.md`, `MANIFEST.md` (+2) |
| 09:11 | `78460b47` | CORRECTION : le gain du SIMD était annoncé ×2,06 ; l'A/B entrelacé donne ×1,18 (passe) et ×1,37 (proj+mlp) | `REPRISE.md`, `plan-deepseek41-complet.md`, `README.md` (+4) |
| 09:39 | `c67e4d01` | analyse_hc.py : le test synthétique a trouvé une faute d'axe (sommer les positions au lieu des colonnes) — corrigé, et les deux cas sont vérifiés (bistochastique -> 0, faux -> 1) | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:10 | `7d5a8fd9` | Réorientation : plan Kimi-K3 — exécuter en local ce qui ne tient pas en local | `plan-kimi-k3.md`, `README.md`, `MANIFEST.md` (+3) |
| 10:27 | `3e2d7014` | Spécification de l'architecture Kimi-K3, tirée de la référence (llama.cpp-k3 + code publié) | `architecture-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 10:43 | `0d8cb93a` | Docs : la cible Kimi-K3, les deux défauts de tokenizer corrigés, et la référence llama.cpp-k3 | `REPRISE.md`, `plan-kimi-k3.md`, `README.md` (+3) |
| 10:44 | `d4b3150b` | Spec Kimi-K3 : cadence hybride VÉRIFIÉE sur le fichier (MLA aux couches 3,7,11,15), détail des projections MLA, MoE latent (routeur en pleine largeur) et res_mix final avant la tête | `architecture-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 11:44 | `d9dc8515` | Sprint 30 : la réutilisation des experts est mesurée — 47-49 % immédiate, un quart de cache sert 80-87 %, plafond 93 % | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 12:03 | `5223a20c` | Journal (màj automatique) | `README.md`, `MANIFEST.md`, `digest.md` (+1) |
| 12:08 | `c357f9cf` | K3 : la passe avant de la couche 0 (f32) — structure d'abord, exactitude ensuite | `kimi_k3.rs`, `README.md`, `MANIFEST.md` (+2) |
| 12:25 | `ca9125c0` | K3 : la couche 0 CALCULE sur le vrai fichier (test de fumée --k3-essai), et il a attrapé une convention de dimensions | `kimi_k3.rs`, `main.rs`, `README.md` (+3) |
| 12:31 | `b34a8e34` | Spec Kimi-K3 : l'ordre exact du MoE latent (routeur en pleine largeur, norme DANS le latent avant la remontée, biais en sélection) | `architecture-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 12:53 | `2514e762` | K3 : le KDA extrait en pièce réutilisable (couches 1, 2, 4, 5, 6, 8…), avec sa remise à zéro d'état | `kimi_k3.rs`, `README.md`, `MANIFEST.md` (+2) |
| 15:03 | `c8ff34c6` | K3 complet : les sorties sont identiques à celles obtenues pendant le transfert | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 15:58 | `af1c3778` | ref_logits_k3 : la commande de liaison est écrite, le binaire n'a plus de mystère | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 16:11 | `ff3a25a0` | REPRISE : le bloc 31 en tête — K3 complet, 86,787 Go par jeton, x1,58 par regroupement | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 16:28 | `07bc7d53` | Tuile : l'essai repris machine au calme confirme la réfutation (20,02 s contre 20,32 s) | `README.md`, `MANIFEST.md`, `digest.md` (+2) |
| 19:45 | `aacb18c3` | K3 : les 13 premières couches, dont la BANQUE de la couche 12 — sorties finies | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+2) |
| 22:57 | `61c8ba5b` | REPRISE : la baseline de la référence (42 min/jeton) et le jalon négatif, en tête | `REPRISE.md`, `README.md`, `MANIFEST.md` (+2) |
| 22:57 | `e2bd0092` | K3 : la référence a tourné — 42 min/jeton, 11 % de CPU, 1,80 To lus pour 4 passes | `verification-kimi-k3.md`, `README.md`, `MANIFEST.md` (+3) |
| 23:45 | `7a5e5d5b` | K3 : deux bugs trouvés par la comparaison — la norme L2 manquante, et la banque qui s'accumulait | `kimi_k3.rs`, `README.md`, `MANIFEST.md` (+2) |

## Chiffres du jour

`11 %` · `20,02 s` · `20,32 s` · `86,787 Go` · `86,787` · `-49 %` · `-87 %` · `93 %` · `×2,06` · `×1,18` · `×1,37` · `60 s`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` — Continue avec REPRISE.md (début 2026-09-28 14:46, 222.5 h) → [rapport](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md) · [digest](../sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md)

## Mesures et rapports touchés

- [reports/rapport-coherence-docs.md](../../reports/rapport-coherence-docs.md)

<!-- notes -->

<!-- /notes -->
