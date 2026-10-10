# 2026-10-09 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-09.md](2026-10-09.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (20)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:07 | `56ef496` | L'échelle par enregistrement des traces : les lecteurs l'ignoraient, et le résultat change | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 01:09 | `4251a4f` | Deux harnais qui manquaient : le protocole 8×128 écrit, l'acceptation mesurée par le moteur | `MANIFEST.md`, `digest.md`, `rapport.md` (+3) |
| 02:31 | `1530bee` | La carte de latence : répartir ne paie que si le calcul dépasse 3,4 ms x RTT | `MANIFEST.md`, `digest.md`, `rapport.md` (+2) |
| 06:53 | `b25c641` | Codestral corrigé, mesuré au protocole commun : 133,08 sur 255 jetons (1,842 bit/octet) | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 09:23 | `eaa17b8` | Trois dessins inédits que Drave récompense : profondeur routée, budget d'événements appris, quantification-aware | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 09:33 | `7041bcc` | Budget d'événements : le premier essai d'allocation ciblée ÉCHOUE, et il apprend pourquoi | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 10:37 | `7f24b33` | Le budget chiffré : 0,4 pJ par événement synaptique contre 0,9 µJ chez nous | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 13:29 | `4878d81` | M1 : le bus de valeur est implémenté, et la valeur auto-référentielle ne suffit pas | `architecture-cerveau-et-drave.md`, `impulsion-pure-apprenant.md`, `MANIFEST.md` (+2) |
| 14:11 | `ed9034e` | M1 dans le moteur : le bus de modulation (nouveauté ou valeur), et la persistance de D | `main.rs`, `model.rs`, `MANIFEST.md` (+2) |
| 17:06 | `59186cf` | C1a : la topologie de régions se lit, se vérifie et refuse les graphes incohérents | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+3) |
| 17:12 | `536256f` | C1b pas 1 : la topologie PILOTE le découpage — porte tenue, même chiffre, 0,00e0 | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+4) |
| 17:35 | `28da341` | C1b pas 2 : le RELAIS — trois régions sur trois instances, écart 0,00e0 | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 17:40 | `daef822` | C12 : trace globale horodatée et rejeu exact — 126 croisements, aucune divergence | `sprint-cerveau.md`, `main.rs`, `trace_globale.rs` (+4) |
| 17:45 | `451b036` | C5 : bus de modulation multi-canaux — canal neutre exact au bit près, canal actif sur un relais | `sprint-cerveau.md`, `bus.rs`, `main.rs` (+4) |
| 21:37 | `517f39b` | C3 : les délais par lien, et le fichier de relations humaines | `relations-humaines.md`, `sprint-cerveau.md`, `main.rs` (+5) |
| 21:46 | `883f934` | C5bis : diffusion du bus par fichier de contrôle — le canal change la région du milieu | `sprint-cerveau.md`, `bus.rs`, `main.rs` (+4) |
| 21:50 | `2924e52` | C4 pas 1 : compteur de pas par région et borne de terminaison explicite | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 21:58 | `6bfb857` | C12bis : le nœud trace, et les traces de plusieurs processus se fusionnent | `sprint-cerveau.md`, `main.rs`, `trace_globale.rs` (+4) |
| 22:12 | `9ae8f6f` | C5ter : le bus par le réseau — un réglage atteint une autre machine | `relations-humaines.md`, `sprint-cerveau.md`, `main.rs` (+4) |
| 23:48 | `22d6151` | C9 x C1 : où couper le modèle — le point de coupe est neutre, sauf à cause du lien | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+4) |

## Chiffres du jour

`255 jetons` · `1,842` · `3,4 ms` · `×128` · `24 couches` · `59,0790` · `9 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Étapes du jour (63)

*Ce que l'agent a consigné en le faisant (lignes `⏵` du journal de session) :*

- **01:40** — Consignation de la mesure à froid du lot sur un MoE (protocole corrigé)
- **02:22** — Correction de l'outil de carte de latence (le batch 2 a échoué dessus)
- **02:23** — Balayage complet de la carte de latence sur deux tailles de modèle
- **10:37** — Ajout du budget énergétique chiffré (cerveau contre notre implémentation)
- **13:25** — M1 : implémentation du bus de modulation par la VALEUR (et non la nouveauté)
- **14:11** — Commit du bus de valeur, puis mise en file de la vérification à l'échelle 512
- **15:34** — Registre des manques publié — et un point d'échelle qui nuance la structure innée
- **17:02** — Lancement du sprint cerveau : objectif autonome, plan, puis première brique (topologie)
- **17:06** — C1a livrée : la topologie se lit, se vérifie, et refuse les graphes incohérents
- **17:11** — C1b pas 1 franchi : la topologie PILOTE le découpage, écart 0,00e0
- **17:13** — C1b pas 1 franchi, porte outillée et tenue — le relais est le prochain jalon
- **17:28** — Cause trouvée : le nœud refuse une plage d'UNE couche — j'utilise un modèle à 24 couches
- **17:33** — Régression réparée (5 modes verts) — je reprends le test du relais
- **17:33** — **C1b pas 2 : le relais est EXACT — trois régions, trois instances, écart 0,00e0**
- **17:36** — **C1 est livrée** : le relais est exact à trois instances — et il a fait trouver un vrai bug
- **17:36** — C12 : la trace globale horodatée et sa vérification par rejeu
- **17:39** — C12 : trace écrite et rejeu identique — je vérifie maintenant qu'une trace FAUSSE est détectée
- **17:39** — C12 : trace exacte, rejeu identique, et trace faussée détectée au pas près
- **17:41** — **C12 livrée** : trace globale au bit près, rejeu sans divergence, et trace fausse détectée
- **17:41** — C5 : le bus de modulation multi-canaux, avec un consommateur qui a des dents
- **17:43** — Le bus neutre est identique (59,0790) — c'est ma porte qui comparait aussi les temps
- **17:44** — Cas 3 : le gain du nœud final est absorbé par la normalisation — je teste sur un nœud RELAIS
- **17:45** — C5 livrée : bus neutre exact au bit près, bus actif sur un nœud relais
- **21:34** — Nouveau mode : timeboxing jusqu'à 9 h demain. Je repars sur C3 — les délais par lien
- **21:38** — C5bis : la diffusion réseau du bus (port de contrôle séparé, sans toucher au protocole de données)
- *(+38 autres étapes — voir les rapports de session)*

## Sessions actives ce jour

- `d31b3d9b` — Où en est-on (début 2026-10-08 09:11, 49.5 h) → [rapport](sessions/d31b3d9b/rapport.md) · [digest](sessions/d31b3d9b/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../reports/rapport-campagne-benefices.md)

<!-- notes -->
` … `
<!-- /notes -->
