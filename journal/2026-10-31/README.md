# 2026-10-31

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-10-31/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**3 commits** · **1 session(s)** · **3 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| docs | 1 | [docs.md](docs.md) |
| modele | 1 | [modele.md](modele.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `22e518ee-81b8-4081-ae1b-f0d7a777a1d7` | Compléter les autres sessions avant le backlog | 2026-10-31 11:13 | 0.2 h | [rapport](../sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/rapport.md) · [digest](../sessions/22e518ee-81b8-4081-ae1b-f0d7a777a1d7/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 11:35 | `eff8d8e4` | SESSIONS — 104 ARCHIVES RETROUVÉES, CINQ CLÔTURES, L'ÉTAT À UNE SEULE SESSION |
| 11:41 | `a2344c84` | ÉTAT — LA CLÔTURE `eff8d8e4` ACTÉE, `22e518ee` CLOSE, N2 DÉSIGNÉE |
| 12:40 | `2edb3079` | JEUX — LE SAN L'EMPORTE SUR LA CASE QUAND UNE POSITION EST FOURNIE (110/112 → 112/112) |

## Le récit de la journée (écrit à la main)

<!-- notes -->
**Les autres sessions d'abord.** Le 30 octobre laissait cinq sessions ouvertes et un état qui
n'en déclarait qu'une. La première tâche du jour n'était pas une ligne de la roadmap : c'était
de **finir les autres**.

**`0b69f616` — les trois chantiers du lecteur.** R0.4 rejouée sur le **corpus gelé** (498 paires) :
**0,540 contre BM25 0,720**, l'écart de 18 points tient après quatre versions et deux corpus —
négatif robuste. R0.5 rejouée sur **331 questions** : le signal monte à **0,839**, mais le
transfert z-score (**0,819 / 0,313**) reste sous le choix fixe (**0,871 / 0,373**) ; close en
négatif, condition nommée. Au passage un **bug de clé** : deux questions de `format-flux.md` ont
le même libellé et deux golds — l'appariement `(document, question)` en écrasait une ; la clé
porte le gold, les 331 questions sont comptées. R13 : la décision est **octets** — BPE 512
**+0,39 %** (bruit, deux graines), 1024 **+4,09 %**, anglais **+4,22 / +6,59 %** ; le « gain de
11 % » du pilote était un **artefact de budget**.

**L'archive ne voyait pas les traces récentes.** Les rapports manquaient pour une raison
mécanique : `archive_sessions.py` et `session_report.py` cherchaient `session.jsonl*`, alors que
DSH écrit `session.v4.jsonl.zstd` depuis fin octobre ; le `pre-commit` les appelait avec
`|| true`, donc l'échec était silencieux. Corrigé dans les trois outils (archivage, rapport,
journal) : le glob couvre les deux noms, `.gitignore` couvre les copies, et `--session` ne
tronque plus l'index. **43 sessions récentes** ont désormais leur digest et leur rapport —
**104 archives** au total.

**Cinq sessions nommées, cinq clôtures.** Les plans passent des dossiers courts aux dossiers
d'**Id complet** ; `N2-GPU` (job GPU sans trace DSH) reçoit un rapport écrit à la main ; les
clôtures de `c3d0f0bd` et `f0969e87` deviennent des `cloture.md`, liens recollés ; `71d57f53`
et `0b69f616` passent à **terminé**. `22e518ee` ouvre la session unique.

**Le graphe et l'état.** **37 fiches**, **42 arêtes dures**, **4 à la frontière** (A2.6, N2, N3,
N4) ; le SVG est régénéré avec le compte et la date justes ; la phrase « 7 items » du récit du 30
est corrigée. `en-cours` ne porte plus qu'une session et nomme la suite : **N2** (la hiérarchie)
ou **N4** (consigne courte) — les GPU sont libres.
<!-- /notes -->
