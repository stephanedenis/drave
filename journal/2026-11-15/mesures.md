# 2026-11-15 — Campagnes et mesures

> **Généré** par `tools/journal_auto.py` (sources : git + `journal/sessions/`).
> Seul le bloc « notes » en fin de fichier est écrit à la main et préservé.
> Heures en **HAE** (EDT, UTC−4), lues dans git. Index du jour : [README.md](README.md). Convention : `docs/methode/organisation-du-depot.md`.

## Commits du jour (15)

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
| 07:04 | `840e613e` | TAGGER — LES CAS D'ERREUR MESURÉS : REFUS D'AUTHENTIFICATION → CODE 4 (AVANT 0), RÉSEAU ET RÉPONSE NON CONFORME → REPLI HEURISTIQUE CODE 0 ; 4/4 CAS, 18/18 CONTRÔLES | `en-cours.md`, `roadmap.md`, `README.md` (+21) |
| 09:18 | `4dbeff45` | SEMAINE 2 — W1 : LE GOLD RÉEL 452 (20 HAND + 432 CORPUS, 242 FR / 210 EN), LE SPLIT 402/H50 FIGÉ, LE SHA256, LES 10 GP/SUB LISTÉS POUR S | `chantiers.md`, `en-cours.md`, `plan-travail.md` (+22) |
| 09:24 | `1683c2b4` | W2 — LE TAGGER SUR 402/H50 : 402 0,9198 → 0,9643 (+4,45), H50 0,6842 → 0,8607 (+17,65) ; F1/ATTACHEMENT 402 INCHANGÉS, FERMÉ 402 −1,55 ; LA RÈGLE NE LE REJETTE PAS (IL GAGNE SUR 402), LA RÉSERVE FERMÉ VA À W3 | `en-cours.md`, `roadmap.md`, `README.md` (+17) |
| 10:59 | `93e046f7` | SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE | `en-cours.md`, `README.md`, `distribue.md` (+18) |
| 12:08 | `9960b37f` | SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN | `en-cours.md`, `roadmap.md`, `README.md` (+27) |
| 13:19 | `e1a28307` | SEMAINE 2 — X3 : LE TAGGER EN LOT (1 000 ITEMS, 662 APPELS RÉSEAU, 98 968 TOKENS, 0,0216 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES) ; --JSONL 1 003 LIGNES | `en-cours.md`, `README.md`, `plan.md` (+5) |

## Chiffres du jour

`0,0216` · `0,5406` · `0,9198` · `0,9643` · `0,6842` · `0,8607` · `0,5270` · `0,092` · `0,160` · `0,811` · `0,657` · `0,440`

*Extraits des sujets de commit et des étapes — le détail et les conditions sont dans la fiche correspondante de `reports/`.*

## Sessions actives ce jour

- `e181ce02-cd50-488a-a6be-e84b79d40dcc` — Documentation Drave avec diagrammes et implémentation (début 2026-10-31 17:40, 357.3 h) → [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md)

## Mesures et rapports touchés

- [reports/INDEX.md](../../reports/INDEX.md)
- [reports/README.md](../../reports/README.md)
- [reports/rapport-atomes-prediction.md](../../reports/rapport-atomes-prediction.md)
- [reports/rapport-bilan-nuit.md](../../reports/rapport-bilan-nuit.md)
- [reports/rapport-cic-v2.md](../../reports/rapport-cic-v2.md)
- [reports/rapport-coordination-n2-v2.md](../../reports/rapport-coordination-n2-v2.md)
- [reports/rapport-exemples-tagger.md](../../reports/rapport-exemples-tagger.md)
- [reports/rapport-faq.md](../../reports/rapport-faq.md)
- [reports/rapport-gold-452.md](../../reports/rapport-gold-452.md)
- [reports/rapport-gold-reel-50.md](../../reports/rapport-gold-reel-50.md)
- [reports/rapport-panini-manifeste.md](../../reports/rapport-panini-manifeste.md)
- [reports/rapport-restitution-v2.md](../../reports/rapport-restitution-v2.md)
- [reports/rapport-restitution-v3.md](../../reports/rapport-restitution-v3.md)
- [reports/rapport-tagger-erreurs.md](../../reports/rapport-tagger-erreurs.md)
- [reports/rapport-tagger-h50.md](../../reports/rapport-tagger-h50.md)
- [reports/rapport-tagger-lot.md](../../reports/rapport-tagger-lot.md)
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

### E2 — les cas d'erreur du tagger : la clé refusée sort 4, le reste replie

Quatre cas, un transport factice, **18/18 tests**, **0 socket**. La **clé absente** sortait déjà
**4** ; la **clé invalide** (HTTP 401/403) rendait **0** avec un repli heuristique muet — elle
sort désormais **4**, message clair, `stdout` vide, sans repli. Le **réseau coupé** (3 essais du
client) et le **refus du modèle** (texte non JSON, JSON incomplet) restent des refus **par
phrase** : repli heuristique, code **0**, cause dans `refus`, POS `source=heuristique`. Un
transport valide donne code **0** et des POS neuronaux (contrôle négatif) ; retirer le contrôle
401/403 fait échouer le test (`0 != 4`). [`fiche`](../../reports/rapport-tagger-erreurs.md) ·
[`JSON`](../../reports/rapport-tagger-erreurs.json).

### W3 — la matrice du tagger : le défaut reste hors ligne, `--tagger` peut seul sortir 4

La **matrice** est mesurée en sous-processus : le **défaut sans clé** sort **0** (heuristique,
`source=heuristique`), **0 socket**, `tools.llm.deepseek` **non importé** ; avec clé, **0**,
**130 tokens** (116 entrée + 14 sortie), **1,156 s**, POS neuronal ; **clé invalide** (401),
**4**, `stdout` **vide**, pas de repli ; **réseau coupé** (connexion refusée réelle), **0** après
**3 essais**, POS heuristique et `refus` publié. Le **coût pour 1 000 phrases** est extrapolé de
W2 : **143 870 tokens**, **989 requêtes**, **981,9 s**, **0,031 $ hors pointe / 0,062 $ en
pointe** ; le cache chaud rejoue à **0 token** en **~0,14 s**. **Recommandation** : défaut hors
ligne, `--tagger` opt-in, **pas de `auto`** ; s'il vient, seulement avec une clé présente et
**sans changer le code de sortie**. **21/21 tests**. [`fiche`](../../reports/rapport-tagger-defaut.md) ·
[`JSON`](../../reports/rapport-tagger-defaut.json).

### W5 — la restitution v3 : les rôles des GP se séparent, le cadre ne suit pas

`_role_gp` quitte la préposition seule pour le **contexte** : `à` + lieu (`la maison`, `Paris`),
`à` + temps (`14 h`, `demain`), `à` + destinataire (`Marie`), `de` + GN (possession) ou + GV
(thème), `avec` + moyen, `par` + passif (agent) ou non (moyen), `en` + temps/lieu/moyen/manière.
Les **24/24** cas de séparation passent. Sur le **gold S** (61 phrases, 144 rôles), la v3 donne
**144/144** et les cinq rôles de la tâche **18/18** (lieu 3, temps 9, destinataire 5, possession 1,
complément 0) — mais le découpage montre **+4 rôles** et **+1 appariement** : le 144/144 n'est pas
un gain de rôles seul. Sur le **gold v2** (46 textes), la v3 ne corrige que le `lieu` : **20/46**
cadres exacts (**17** non vides) contre 19/46, F1 **0,5406** contre 0,5270, `lieu` F1 **0,60**
contre 0,40 ; `agent` et `prédicat` sont inchangés. Le **contrôle négatif** tue la mesure :
permutation des cinq rôles **0/18**, permutation de tous **0,4028** global, rôle constant `lieu`
**0,0208** (3/18, F1 0,037). `--roles-v3` est le mode ; `--roles` reste la v2. Verdict :
**positif sur la séparation, négatif sur le produit** — la segmentation et le choix du cadre
pèsent plus que la préposition. [`fiche`](../../reports/rapport-restitution-v3.md) ·
[`JSON`](../../reports/pensee-restitution-v3.json).
<!-- /notes -->
