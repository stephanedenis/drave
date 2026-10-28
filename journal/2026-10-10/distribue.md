# 2026-10-10 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (26)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:50 | `19a4a012` | Porte bus-socket : elle rendait 1 en ayant TOUT réussi (sys.exit avec un message) | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 05:48 | `203872af` | C10 : budget d'octets par lien — déclaré dans la topologie, vérifié sur ce qui PASSE | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+5) |
| 05:56 | `619b9405` | C11 : pannes de lien nommees, code distinct, et jamais de resultat partiel | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+4) |
| 06:05 | `47b2ad6d` | C10 (suite) : budget de LATENCE par lien — troisieme volet des budgets du plan | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+5) |
| 07:21 | `c43425e9` | La porte rouge de repartition : c'etait un DEFAUT DE PORTE, pas du modele | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+3) |
| 07:25 | `b1b63b0a` | C11 (decouverte) : le registre des regions — les topologies ne codent plus les adresses | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+4) |
| 07:55 | `6d9bc74f` | Verification apres le changement de type de ffn_gain : porte-flux verte, reference inchangee | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:09 | `719ab855` | Defaut trouve et corrige : --ffn-gain ne faisait RIEN dans le chemin reparti | `sprint-cerveau.md`, `main.rs`, `MANIFEST.md` (+4) |
| 08:35 | `c23f43fa` | Protocole v7 specifie a l'octet pres, et PAS implemente : le round qui le fera doit avoir de la marge | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:35 | `671b4b4d` | Verification apres le refus des reglages non transportables : flux, pannes et registre vertes | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:39 | `af6d5667` | Protocole v7 tente et REVERTE : neuf tests encodent la mise en page v6 | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:55 | `6df044f5` | Verification du protocole v7 sur toutes les portes reparties : huit vertes | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 08:56 | `1a6ce844` | Protocole v8 specifie : le compte de PAIRES du noeud, et sa difficulte propre | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 09:01 | `e22dbd76` | PROTOCOLE v8 LIVRE : le compte de paires du noeud voyage, et le chiffre a attrape mon bug | `sprint-cerveau.md`, `main.rs`, `model.rs` (+4) |
| 09:07 | `957bf34f` | Budget de paires : tente et REVERTE — deux lecons, dont une donnee par la porte | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 09:10 | `4767b220` | C10 CLOS : trois budgets, trois codes — octets (6), latence (8), paires (9) | `sprint-cerveau.md`, `main.rs`, `topologie.rs` (+5) |
| 09:11 | `43670993` | Etalonnage de l'instrument de trace : 50 ms injectes, 50,2 ms mesures | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:12 | `d09f78c7` | La GIGUE d'un pas reparti : 7 ms sur 17,7 (40 %) — ce qu'un ordonnanceur doit tolerer | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:13 | `c4bb56a3` | La gigue avec un VRAI RTT : 14,8 ms sur 30,2 (49 %) — elle croit plus vite que la latence | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:15 | `656a65fa` | Combien de MESSAGES coute un pas ? Quatre — et c'est l'en-tete ecrit a part | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 09:30 | `c749af23` | Verification apres v7/v8 et la fusion des ecritures : huit portes reparties vertes | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+1) |
| 09:39 | `63203d79` | Inventaire des drapeaux en reparti : cinq agissent, trois inertes (deux attendus), un ouvert | `sprint-cerveau.md`, `MANIFEST.md`, `digest.md` (+2) |
| 10:56 | `33676cb6` | Journal : etapes DATEES par la trace de session (elles couvraient toute la session) | `2026-10-09_attention.md`, `2026-10-09_distribue.md`, `2026-10-09_divers.md` (+22) |
| 13:16 | `eac873a3` | C8 : la tete reflexe generalise (x5,7 du modele complet) — et deux pieges de protocole corriges | `etat-cerveau.md`, `2026-10-10.md`, `2026-10-10_apprentissage.md` (+17) |
| 20:10 | `97086a11` | Registre des manques : N5 — le modele ne retient pas un signal injecte (mesure : present 0,992 / passe -0,681 / tampon 1,000) | `manques.md`, `2026-10-10.md`, `2026-10-10_distribue.md` (+5) |
| 23:53 | `2ef2774a` | Instrument : le compteur de paires du moteur ne voit PAS l'elagage des poids, sur aucun chemin | `modele-pour-drave.md`, `2026-10-10.md`, `2026-10-10_apprentissage.md` (+14) |

## Chiffres du jour

`0,992` · `0,681` · `1,000` · `49 %` · `14,8 ms` · `40 %` · `7 ms` · `50 ms` · `50,2 ms`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` — Où en est-on (début 2026-10-08 09:11, 71.0 h) → [rapport](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/rapport.md) · [digest](../sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md)

## Mesures et rapports touchés

- [reports/rapport-c8-generalisation.md](../../reports/rapport-c8-generalisation.md)
- [reports/rapport-campagne-benefices.md](../../reports/rapport-campagne-benefices.md)
- [reports/rapport-e6-poids-lognormaux.md](../../reports/rapport-e6-poids-lognormaux.md)

<!-- notes -->
` … `
<!-- /notes -->
