# Roadmap native — DRVM, `drave-n0`, distillation

> **Programme N**, prioritaire sur B9/B10/B11 comme **ligne principale**. B9/B10/B11 deviennent
> des **bancs de mesure** du natif, pas la base à adapter. Décision d'architecture :
> [`architecture-native.md`](../theorie/architecture-native.md). Aucune date ; un chantier est
> fini quand il est mesuré, écrit et committé.

## Le principe

**Repartir à neuf, pas à zéro.** On garde le moteur, le bus, DRVF, les portes, les mesures et
l'outillage ; on remplace la **base** — GGUF, Qwen3-MoE, le modèle monolithique — par un
**format** (DRVM) et un **modèle** (`drave-n0`) conçus pour les mécanismes Drave.

## Les cinq phases

| phase | livrable | ce qui est mesuré | ce qui est explicitement **hors** |
|---|---|---|---|
| **N0 — le format** | DRVM v0 : manifeste, graphe, blocs, routes, contrats, hash | aller-retour, `mmap`, chargement `drave-core`, import GGUF | pas d'entraînement |
| **N1 — le modèle v0** | `drave-n0` 12 M, 6 blocs, têtes précoces, pensée, pont | parité entraîneur ↔ moteur, réflexe, λ < 1, contenu | pas de chat |
| **N2 — la distillation** | 50 000 séquences, professeur Qwen/DeepSeek, pertes locales | écart au professeur, 30 langues, tenue à l'écart | pas de service |
| **N3 — les opérations** | k-WTA, routes, sorties précoces, pont, rejeu, placement | qualité/octets, temps, trace identique | pas de chat |
| **N4 — l'usage** | SFT instruction, BPE ou octets, serveur, sûreté | suivi d'instructions, arrêt, multi-tours | pas de scale |
| **N5 — l'échelle** | 50–100 M, corpus élargi | les mêmes portes, à l'échelle | — |

## N0 — le format DRVM (1 semaine)

**Pourquoi d'abord** : tant que le modèle ne peut pas être **écrit**, **lu** et **rejoué** par le
moteur, tout entraînement est un banc hors moteur. C'est le chaînon manquant déjà constaté
([`rapport-modele-drave.md`](../../reports/rapport-modele-drave.md) §6).

| # | chantier | critère |
|---|---|---|
| N0.1 | Écrire le manifeste et le graphe (blocs, ports, routes, têtes, pont, pensée) | ✅ **fait** — manifeste JSON canonique, graphe, hash vérifié |
| N0.2 | Écrire le payload tenseurs (alignement, quantification, masque de sparsité) | ✅ **fait** — aller-retour octet-à-octet, 64 o |
| N0.3 | Lire DRVM dans `drave-core` | ✅ **PPL DRVM en mémoire** — `drvm.rs` lit l'en-tête, le graphe, les tenseurs ; `--drvm-ppl` calcule **28,7355** sans fichier temporaire (via `Gguf::depuis_octets`) ; **114/114** tenseurs identiques |
| N0.4 | `gguf2drvm` et `drvm2gguf` pour les modèles existants | ✅ **mesuré** — Qwen 0.5B Q4_0 : 290 tenseurs, **SHA identique** en aller-retour sur 337 Mo |
| N0.5 | Trace et rejeu d'un bloc DRVM | ✅ **mesuré** — contenu **291/291**, trace **6 144 listes**, rejeu **0 manquante**, logits **SHA identique**, PPL **28,7355** |
| N0.6 | Refus de version et de bloc inconnu | ✅ **fait** — version 99 et bloc `quantum` refusés |

**Porte N0** : un modèle DRVM de test (petit, aléatoire) est **écrit**, **lu**, **exécuté** et
**rejoué** par le moteur, sans conversion. **État : partiel** — écrit, lu et vérifié en Python
(6 tests) ; l'exécution par `drave-core` (N0.3) lit le conteneur ; la **parité de perplexité** avec un GGUF reste la porte bloquante.

## N1 — `drave-n0` (2–3 semaines)

**Le modèle** : 12 M, 6 blocs, deux régions, octets.

| # | chantier | critère |
|---|---|---|
| N1.1 | Famille `native` dans l'entraîneur (blocs, routes, têtes précoces) | ✅ **architecture** — `tools/native_model.py`, 11,37 M, 6 blocs, 3 têtes, 4 tests de forme ; **entraînement 200 pas à faire** |
| N1.2 | Entraînement next-byte sur corpus propre | ⏳ **à faire** — PPL < 4,0 sur tenu à l'écart |
| N1.3 | Export DRVM et chargement moteur | ✅ **export** — 114 tenseurs, `drave --drvm-inspect` lit 12 blocs ; **114/114 identiques** au checkpoint ; **parité PPL à faire** |
| N1.4 | Têtes précoces (blocs 2, 4, 6) | ✅ **mesuré** — **55,15 / 60,94 / 62,13 %** contre **62,55 %** pour la principale, témoin **0,39 %** ; PPL 3,363 |
| N1.5 | Cellule de pensée contractante | ✅ **mesuré** — **λ = 0,709** ; PPL sans pensée **721 726**, avec **3,53** ; PPL **3,58** |
| N1.7 | **Vitesse du réflexe** | ✅ **mesuré** — 4 blocs **5,978 ms** contre 6 blocs **7,871 ms**, gain **24,05 %**, coût **−1,61 point** de précision |
| N1.6 | Pont de région | ✅ **mesuré** — PPL **3,465**, neutralisé **4,080** ; effet **−9,3 %** ; coût vs modèle sans pont **−3,2 %** |

**Porte N1** : `drave-n0` est un **banc de mécanismes** mesuré dans le moteur ; il ne parle pas
encore. **État : architecture + export faits ; entraînement et mesures à faire.**

## N2 — distillation et données (3–4 semaines)

**Le corpus** : 610 → **50 000 séquences**, avec un jeu tenu à l'écart et un contrôle par
permutation.

| # | chantier | critère |
|---|---|---|
| N2.1 | Collecte et filtrage (UDHR, textes publics, code, dialogue) | ⚠️ **volume** — 50 000 fenêtres, 45 000/5 000 ; **un seul corpus**, licence à vérifier, diversité non faite |
| N2.2 | Professeur local (Qwen 0.5B, logits) + DeepSeek (séquences) | deux sources, pas une seule |
| N2.3 | Distillation + pertes locales + têtes + pensée | écart ≤ **4,40 %** (B9) |
| N2.4 | Contrôle 30 langues | pas de chute > 5 pts |
| N2.5 | Contrôle par permutation | le modèle ne suit pas l'étiquette mélangée |
| N2.6 | Ablation : sans perte locale, sans tête, sans pensée | chaque perte paie ou est retirée |

**Porte N2** : le natif **bat ou égale** B9 (4,40 %) sur le même corpus, avec les pertes natives.

## N3 — les opérations natives (3–4 semaines)

| # | chantier | critère |
|---|---|---|
| N3.1 | k-WTA 25 % et routes explicites | même PPL, moins d'octets |
| N3.2 | Sortie précoce en production (réflexe) | accord mesuré, pas un vœu |
| N3.3 | Pont et régions | coupe à un bon endroit (A7) |
| N3.4 | Rejeu DRVM | trace identique, mêmes logits |
| N3.5 | Placement par bloc (GPU/CPU/réseau) | le moins cher où ça tient |
| N3.6 | Démonstration distante | un bloc DRVM exécuté à distance |

**Porte N3** : les mécanismes Drave sont **mesurés dans le moteur**, pas seulement dans
l'entraîneur.

## N4 — l'usage (4–6 semaines)

| # | chantier | critère |
|---|---|---|
| N4.1 | Décision **octets vs BPE** | mesurée, pas idéologique |
| N4.2 | SFT instruction (chat, arrêt, système) | suivi d'instructions > baseline |
| N4.3 | Serveur OpenAI-compatible + streaming | un client standard se connecte |
| N4.4 | Sûreté et refus | refus explicite, pas de fuite |
| N4.5 | Évaluation externe | MMLU minimal, chrF, latence |

**Porte N4** : « utilisable » = un assistant qui **répond**, **s'arrête**, **suit une consigne**
et **sert** sur une API ; pas seulement un banc.

## N5 — l'échelle (continu)

- **50–100 M**, corpus élargi, BPE si N4.1 le justifie.
- Les portes N0–N4 sont **repassées** à l'échelle ; aucune n'est supposée acquise.
- Le professeur n'est plus la béquille : le modèle doit tenir **sans distillation** sur une
  partie du corpus.

## Ce qui change dans la roadmap existante

| ligne | avant | après |
|---|---|---|
| **B9** | élève natif = but | **banc** de distillation du programme N |
| **B10** | protocole sémantique | **banc** du décodeur et de `z` |
| **B11** | base typée | **banc** du RSN et du codec |
| **A7** | grappe déportée | **support** de N3.5/N3.6 |
| **B12** | modules cerveau | **mesures** des mécanismes, pas la base du modèle |
| **nouveau N** | — | **ligne principale** |

## Les questions ouvertes

- **Format** : CBOR ou JSON compact pour le manifeste ? **Décision N0.1**, pas avant.
- **Modèle** : 6 blocs suffisent-ils pour que le pont paie ? **Mesure N1.6**.
- **Données** : 50 000 séquences sont-elles accessibles et licites ? **N2.1**.
- **BPE** : le coût des octets est-il acceptable à 12 M ? **N4.1**.
- **Professeur** : logits Qwen 0.5B + séquences DeepSeek suffisent-ils ? **N2.2**.

## La prochaine action

**N0.1** : écrire le manifeste DRVM et le graphe d'un modèle de test, avec un lecteur qui refuse
une version inconnue. **Aucun entraînement avant que N0.3 soit vert.**
