# 2026-11-15 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (9)

| heure | commit | fait | fichiers |
|---|---|---|---|
| 01:39 | `2d7a7f2b` | 1A — LES DEUX DÉFAUTS DU TAGGER CORRIGÉS : 1 APPEL PAR PHRASE (LE TAGGER DE SYNTAGMES RETIRÉ) ET PONCT RESTITUÉ (25/25) ; POS 612 → 95,75 % (+9,5) | `en-cours.md`, `README.md`, `portes.md` (+9) |
| 01:42 | `6560a0a5` | 1A — LE TAGGER SUR LA BASE RÉELLE : 88,91 → 95,00 % (+6,1), 449 APPELS SERVIS PAR LE CACHE ; IL GAGNE SURTOUT SUR LE SYNTHÉTIQUE (+9,5 SUR 612) | `en-cours.md`, `README.md`, `mesures.md` (+7) |
| 02:13 | `292c70b5` | C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09 | `en-cours.md`, `README.md`, `docs.md` (+13) |
| 03:48 | `011b8b8e` | B2 — LES ATOMES NE PRÉDISENT PAS POS, SYNTAGMES NI ATTACHEMENT : SUR 28 ŒUVRES PROPRES, R² −0,092 / −0,160 / −0,092 (p 0,56 / 0,85 / 0,67) ; LE STYLE EST PRÉDIT (GRAPHÈMES +0,811, MOTS +0,657, NÉGATION +0,440, VERBES +0,429) MAIS ABSORBÉ PAR LA DATE (p_resid 0,76–1,0) | `en-cours.md`, `roadmap.md`, `README.md` (+18) |
| 04:03 | `2067a6f0` | B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS | `en-cours.md`, `roadmap.md`, `README.md` (+18) |
| 04:33 | `ee04ea91` | BILAN DE LA NUIT — LE TAGGER (95,75), LA BASE HONNÊTE (452), LA PHASE C/B (N2, S, R, PANINI) ET LES NÉGATIFS DITS | `en-cours.md`, `README.md`, `distribue.md` (+11) |
| 04:46 | `d23780d7` | D1 — LES EXEMPLES DU TAGGER ET DE LA BASE RÉELLE : 3 BLOCS --tagger (441 TOKENS, 3,7 S), 2 BLOCS --reel (452 PHRASES, POS 88,91, F1 79,06), 5/5 REJOUÉS, MUTATION 4/5 | `en-cours.md`, `roadmap.md`, `README.md` (+16) |
| 06:08 | `5b2d07fc` | D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270) | `en-cours.md`, `roadmap.md`, `README.md` (+26) |
| 06:20 | `4d6cffc4` | PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS | `en-cours.md`, `README.md`, `distribue.md` (+15) |

## Chiffres du jour

`0,5270` · `0,092` · `0,160` · `0,811` · `0,657` · `0,440` · `0,429` · `2,7856` · `40,0658` · `95,00 %` · `95,75 %`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 349.8 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/rapport-atomes-prediction.md](../../reports/rapport-atomes-prediction.md)
- [reports/rapport-bilan-nuit.md](../../reports/rapport-bilan-nuit.md)
- [reports/rapport-cic-v2.md](../../reports/rapport-cic-v2.md)
- [reports/rapport-coordination-n2-v2.md](../../reports/rapport-coordination-n2-v2.md)
- [reports/rapport-exemples-tagger.md](../../reports/rapport-exemples-tagger.md)
- [reports/rapport-faq.md](../../reports/rapport-faq.md)
- [reports/rapport-gold-reel-50.md](../../reports/rapport-gold-reel-50.md)
- [reports/rapport-restitution-v2.md](../../reports/rapport-restitution-v2.md)
- [reports/rapport-tagger-option.md](../../reports/rapport-tagger-option.md)

<!-- notes -->
### D2 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas

La v2 devait passer de la surface (v0) et de la forme canonique (v1) aux **rôles**. Elle le fait
comme **forme** : `restituer --roles` rend un cadre `agent / prédicat / lieu`, 198 segments de rôle,
**198/198** spans dans la source, et `relire_roles(rendre_roles(a))` redonne le cadre **46/46**.
Mais la **fidélité** ne suit pas. Sur un or écrit à la main (46 cadres, 65 variantes), **19/46**
cadres sont exacts — **16/46** non vides —, **91/138** cellules exactes, mais **F1 0,5270**
(précision 0,5493, rappel 0,5065, **32 faux positifs / 38 faux négatifs**) ; **agent 0,6000**,
**prédicat 0,4872**, **lieu 0,4000**. Les planchers : vide **7/46**, constant par type **6/46**,
rôles mélangés **3/46**. Le contrôle externe (gold S, 61 phrases) vaut **139/144 = 0,9653** :
l'instrument n'est pas cassé ; c'est la lecture des rôles de l'annotation qui ne tient pas.
`f03` lit `Comment / Bonjour`, `f20` lit `Leroy / M / vers 9 h`, `f27` (« Élodie sourit. ») n'a
aucun syntagme. La v2 est une **vue fidèle de rôles souvent faux ou absents**, pas un analyseur.
[`fiche`](../../reports/rapport-restitution-v2.md) · [`JSON`](../../reports/pensee-restitution-v2.json).

### D3 — la FAQ : dix questions, dix réponses vérifiées

La notice produit gagne une **FAQ** (§ 8) : langue, hors-ligne, coût, tagger, schéma,
attachement, spans inatteignables, restitution, limites, installation. Ce n'est pas une mesure
nouvelle : **dix contrôles** rejouent le CLI et lisent les JSON publiés. **10/10** passent ; le
**contrôle négatif** est détecté (le CLI refuse `--langue de`, le schéma v2 refuse une annotation
v1). Les chiffres cités restent ceux des fiches : **238/239** cibles (**0,9958**), `g017`
([9:28] attendu / [9:38] prédit, règle **rejetée**, F1 **0,7901**), restitution v0 **46/46**,
v1 **46/46**, v2 **19/46** cadres (**16** non vides, F1 **0,5270**), tagger **609 appels /
22 299 tokens / 155 s / ~0,02 $**. Le vérificateur est
[`tools/verifier_faq.py`](../../tools/verifier_faq.py), le relevé
[`faq.json`](../../reports/faq.json), la fiche
[`rapport-faq.md`](../../reports/rapport-faq.md).
<!-- /notes -->
