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

`255 jetons` · `1,842` · `3,4 ms` · `×128` · `50 ms` · `50,2 ms` · `40 %` · `7 ms` · `49 %` · `14,8 ms` · `4 messages`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Étapes du jour (25)

*Ce que l'agent a consigné en le faisant (lignes `⏵` du journal de session) :*

- Campagne 24 h lancée : file de mesures + deux paires d'entraînement en parallèle
- Registre des manques publié — et un point d'échelle qui nuance la structure innée
- C1b pas 1 franchi, porte outillée et tenue — le relais est le prochain jalon
- **C1 est livrée** : le relais est exact à trois instances — et il a fait trouver un vrai bug
- **C12 livrée** : trace globale au bit près, rejeu sans divergence, et trace fausse détectée
- Round 7 livré : C10 fermé — budget par lien, vérifié sur ce qui passe
- Round 8 livré : C11 — les pannes sont nommées, avec leur propre code
- Round 9 livré : C10 complet (octets **et** latence), quatre codes d'arrêt distincts
- Round 11 : la rouge était la PORTE — et notre modèle entraîné survit au découpage
- Round 12 livré : C11 — le registre des régions, la « découverte » du plan
- Round 16 livré : le déséquilibre E/I est **localisé à l'entrée**, pas réparti
- Round 20 livré : un drapeau qui ne faisait **rien** dans le chemin réparti — trouvé, corrigé, gardé
- Round 26 livré : le protocole v7 **spécifié à l'octet près** — et explicitement pas implémenté
- Round 27 livré : protocole v7 tenté puis **reverté** — neuf tests encodent la mise en page v6
- Round 29 livré : le v7 vérifié sur **toutes** les portes réparties — huit vertes
- Round 30 livré : protocole v8 **spécifié** — le compte de paires du nœud
- Round 31 livré : **protocole v8** — le compte de paires du nœud voyage, et le chiffre a attrapé mon bug
- Round 32 livré : budget de paires **tenté et reverté** — deux leçons, dont une donnée par la porte
- Round 33 livré : **C10 CLOS** — trois budgets de lien, trois codes d'arrêt distincts
- Round 34 livré : l'instrument de trace est **étalonné** — 50 ms injectés, 50,2 ms mesurés
- Round 35 livré : la **gigue** d'un pas réparti — 7 ms sur 17,7, soit 40 %
- Round 36 livré : la gigue avec un **vrai RTT** — 14,8 ms sur 30,2 (49 %)
- Round 37 livré : un pas coûte **4 messages** — l'en-tête est écrit à part du corps
- Round 40 livré : vérification après v7/v8 et la fusion des écritures — **huit portes réparties vertes**
- Round 43 livré : inventaire **définitif** des drapeaux en réparti — six sur dix agissent, un seul candidat ouvert

## Sessions actives ce jour

- `d31b3d9b` — Où en est-on (début 2026-10-08 09:11, 49.5 h) → [rapport](sessions/d31b3d9b/rapport.md) · [digest](sessions/d31b3d9b/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../reports/rapport-campagne-benefices.md)

<!-- notes -->
` … `
<!-- /notes -->
