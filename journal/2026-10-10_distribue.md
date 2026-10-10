# 2026-10-10 — Régions, flux, protocoles, budgets, pannes

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [2026-10-10.md](2026-10-10.md). Convention : `docs/organisation-du-depot.md`.

## Commits du jour (23)

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
| 10:56 | `33676cb` | Journal : etapes DATEES par la trace de session (elles couvraient toute la session) | `2026-10-09_attention.md`, `2026-10-09_distribue.md`, `2026-10-09_divers.md` (+22) |

## Chiffres du jour

`49 %` · `14,8 ms` · `40 %` · `7 ms` · `50 ms` · `50,2 ms` · `256 jetons` · `255 jetons` · `5,3719` · `14,6496` · `18,5520` · `12 couches`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Étapes du jour (95)

*Ce que l'agent a consigné en le faisant (lignes `⏵` du journal de session) :*

- **00:04** — Le seul lien FPGA est un FT232H — je vérifie ce qui est réellement derrière
- **00:39** — C2 : je trace l'injection pour voir si elle s'exécute réellement
- **00:57** — C2 : je trace l'injection à l'exécution pour trancher (mon raisonnement l'exige)
- **01:43** — Une porte est rouge (`porte-bus-socket`, code 1 sans marqueur) — j'attends la fin puis j'enquête
- **01:47** — Vrai défaut : `sys.exit("message")` sort en code 1 même quand la porte réussit
- **01:47** — Je corrige le motif (`sys.exit` avec un message sort toujours en 1) et relance la porte
- **02:02** — Une apostrophe inversée a mangé un mot de mon message de commit — je vérifie et corrige
- **02:16** — Résultat NON robuste : un point d'interrogation de plus fait passer la distance de 136 à 378 — je corrige mon propre excès
- **04:08** — Porte verte (5/5) — je corrige le message de clôture resté périmé et je commite
- **05:45** — C10 : je clôture les budgets par lien — déclaration dans la topologie, refus si dépassée
- **05:47** — C10 : porte 3/3 verte — budget déclaré, dépassement nommé, code 6, aucun résultat partiel
- **05:48** — Round 7 livré : C10 fermé — budget par lien, vérifié sur ce qui passe
- **05:49** — C11 : les pannes — nommer la région et le pas, code distinct, jamais de résultat partiel
- **05:53** — Le nœud du cas 2 n'a pas démarré (port en TIME_WAIT) — je donne un port par cas
- **05:55** — La porte attendait un événement fragile — je la rends robuste (pilote en fond, mort chronométrée)
- **05:56** — C11 : porte 3/3 verte — je commite et je relance porte-flux (chemin d'exécution touché)
- **06:01** — porte-flux 5/5 verte après les changements ; je vérifie la porte budget qui partage le chemin
- **06:01** — Round 8 livré : C11 — les pannes sont nommées, avec leur propre code
- **06:01** — C10 (suite) : le budget de LATENCE par lien — le troisième volet des budgets du plan
- **06:05** — Round 9 livré : C10 complet (octets **et** latence), quatre codes d'arrêt distincts
- **07:19** — 19 portes vertes, 1 rouge (`porte-reparti-moteur`) — même motif que bus-socket ?
- **07:20** — Hypothèse protocole : je compare le NOMBRE DE JETONS notés par les deux chemins
- **07:20** — TROUVÉ : le fichier a 256 jetons ; `--ppl` note les 128 PREMIERS, `--ppl-reparti` les 128 DERNIERS
- **07:21** — Round 11 : la rouge était la PORTE — et notre modèle entraîné survit au découpage
- **07:21** — C11 (découverte) : le registre de régions — les topologies ne codent plus les adresses en dur
- *(+70 autres étapes — voir les rapports de session)*

## Sessions actives ce jour

- `d31b3d9b` — Où en est-on (début 2026-10-08 09:11, 51.4 h) → [rapport](sessions/d31b3d9b/rapport.md) · [digest](sessions/d31b3d9b/digest.md)

## Mesures et rapports touchés

- [reports/rapport-campagne-benefices.md](../reports/rapport-campagne-benefices.md)

<!-- notes -->
` … `
<!-- /notes -->
