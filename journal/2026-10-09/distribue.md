# 2026-10-09 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (19)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:07 | `56ef4967` | L'échelle par enregistrement des traces : les lecteurs l'ignoraient, et le résultat change | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 01:09 | `4251a4fd` | Deux harnais qui manquaient : le protocole 8×128 écrit, l'acceptation mesurée par le moteur | `MANIFEST.md`, `digest.md`, `rapport.md` (+3) |
| 02:31 | `1530beef` | La carte de latence : répartir ne paie que si le calcul dépasse 3,4 ms x RTT | `MANIFEST.md`, `digest.md`, `rapport.md` (+2) |
| 06:53 | `b25c641e` | Codestral corrigé, mesuré au protocole commun : 133,08 sur 255 jetons (1,842 bit/octet) | `MANIFEST.md`, `digest.md`, `rapport.md` (+1) |
| 09:23 | `eaa17b85` | Trois dessins inédits que Drave récompense : profondeur routée, budget d'événements appris, quantification-aware | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 09:33 | `7041bcca` | Budget d'événements : le premier essai d'allocation ciblée ÉCHOUE, et il apprend pourquoi | `modele-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 10:37 | `7f24b33b` | Le budget chiffré : 0,4 pJ par événement synaptique contre 0,9 µJ chez nous | `biologie-pour-drave.md`, `MANIFEST.md`, `digest.md` (+1) |
| 13:29 | `4878d811` | M1 : le bus de valeur est implémenté, et la valeur auto-référentielle ne suffit pas | `architecture-cerveau-et-drave.md`, `impulsion-pure-apprenant.md`, `MANIFEST.md` (+2) |
| 17:06 | `59186cf2` | C1a : la topologie de régions se lit, se vérifie et refuse les graphes incohérents | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+3) |
| 17:12 | `536256f9` | C1b pas 1 : la topologie PILOTE le découpage — porte tenue, même chiffre, 0,00e0 | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+4) |
| 17:35 | `28da341a` | C1b pas 2 : le RELAIS — trois régions sur trois instances, écart 0,00e0 | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 17:40 | `daef8222` | C12 : trace globale horodatée et rejeu exact — 126 croisements, aucune divergence | `sprint-cerveau.md`, `main.rs`, `trace_globale.rs` (+4) |
| 17:45 | `451b036e` | C5 : bus de modulation multi-canaux — canal neutre exact au bit près, canal actif sur un relais | `sprint-cerveau.md`, `bus.rs`, `main.rs` (+4) |
| 21:37 | `517f39b6` | C3 : les délais par lien, et le fichier de relations humaines | `relations-humaines.md`, `sprint-cerveau.md`, `main.rs` (+5) |
| 21:46 | `883f934e` | C5bis : diffusion du bus par fichier de contrôle — le canal change la région du milieu | `sprint-cerveau.md`, `bus.rs`, `main.rs` (+4) |
| 21:50 | `2924e52e` | C4 pas 1 : compteur de pas par région et borne de terminaison explicite | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+3) |
| 21:58 | `6bfb857e` | C12bis : le nœud trace, et les traces de plusieurs processus se fusionnent | `sprint-cerveau.md`, `main.rs`, `trace_globale.rs` (+4) |
| 22:12 | `9ae8f6f3` | C5ter : le bus par le réseau — un réglage atteint une autre machine | `relations-humaines.md`, `sprint-cerveau.md`, `main.rs` (+4) |
| 23:48 | `22d61516` | C9 x C1 : où couper le modèle — le point de coupe est neutre, sauf à cause du lien | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+4) |

## Chiffres du jour

`255 jetons` · `1,842` · `3,4 ms` · `×128`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` — Où en est-on (début 2026-10-08 09:11, 71.0 h) → [rapport](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md) · [digest](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../../reports/rapport-campagne-benefices.md)

<!-- notes -->
` … `
<!-- /notes -->
