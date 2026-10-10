# 2026-10-10 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-10.md](2026-10-10.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (22)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:50 | `19a4a01` | Porte bus-socket : elle rendait 1 en ayant TOUT réussi (sys.exit avec un message) | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 05:48 | `203872a` | C10 : budget d'octets par lien — déclaré dans la topologie, vérifié sur ce qui PASSE | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+5) |
| 05:56 | `619b940` | C11 : pannes de lien nommees, code distinct, et jamais de resultat partiel | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+4) |
| 06:05 | `47b2ad6` | C10 (suite) : budget de LATENCE par lien — troisieme volet des budgets du plan | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+5) |
| 07:21 | `c43425e` | La porte rouge de repartition : c'etait un DEFAUT DE PORTE, pas du modele | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+3) |
| 07:25 | `b1b63b0` | C11 (decouverte) : le registre des regions — les topologies ne codent plus les adresses | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+4) |
| 07:55 | `6d9bc74` | Verification apres le changement de type de ffn_gain : porte-flux verte, reference inchangee | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:09 | `719ab85` | Defaut trouve et corrige : --ffn-gain ne faisait RIEN dans le chemin reparti | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+4) |
| 08:35 | `c23f43f` | Protocole v7 specifie a l'octet pres, et PAS implemente : le round qui le fera doit avoir de la marge | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:35 | `671b4b4` | Verification apres le refus des reglages non transportables : flux, pannes et registre vertes | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:39 | `af6d566` | Protocole v7 tente et REVERTE : neuf tests encodent la mise en page v6 | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:55 | `6df044f` | Verification du protocole v7 sur toutes les portes reparties : huit vertes | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:56 | `1a6ce84` | Protocole v8 specifie : le compte de PAIRES du noeud, et sa difficulte propre | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 09:01 | `e22dbd7` | PROTOCOLE v8 LIVRE : le compte de paires du noeud voyage, et le chiffre a attrape mon bug | `sprint-cerveau.md`, `main.rs`, `model.rs` (+4) |
| 09:07 | `957bf34` | Budget de paires : tente et REVERTE — deux lecons, dont une donnee par la porte | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 09:10 | `4767b22` | C10 CLOS : trois budgets, trois codes — octets (6), latence (8), paires (9) | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+5) |
| 09:11 | `4367099` | Etalonnage de l'instrument de trace : 50 ms injectes, 50,2 ms mesures | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:12 | `d09f78c` | La GIGUE d'un pas reparti : 7 ms sur 17,7 (40 %) — ce qu'un ordonnanceur doit tolerer | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:13 | `c4bb56a` | La gigue avec un VRAI RTT : 14,8 ms sur 30,2 (49 %) — elle croit plus vite que la latence | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:15 | `656a65f` | Combien de MESSAGES coute un pas ? Quatre — et c'est l'en-tete ecrit a part | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:30 | `c749af2` | Verification apres v7/v8 et la fusion des ecritures : huit portes reparties vertes | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 09:39 | `63203d7` | Inventaire des drapeaux en reparti : cinq agissent, trois inertes (deux attendus), un ouvert | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |

## Sessions actives ce jour

- `d31b3d9b` — Où en est-on (début 2026-10-08 09:11, 49.3 h) → [rapport](sessions/d31b3d9b/rapport.md) · [digest](sessions/d31b3d9b/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../reports/rapport-campagne-benefices.md)

<!-- notes -->
` … `
<!-- /notes -->
