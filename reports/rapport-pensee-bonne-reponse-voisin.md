# B13 — la bonne réponse, pas le voisin : lien auto 2/5, contextuel 5/5 (distracteurs r428–r432)

> **Ligne de roadmap** : **L/B13** · **Date** : 2026-11-03 · **Verdict** : ⚠️ **le lien automatique
> choisit le voisin** — sur les 5 questions pièges (r418–r422), le lien automatique
> (`trouver_precedente`, le plus récent partageant le sujet) trouve **2/5** ; la réponse
> **contextuelle** (`repondre_contextuel` à partir de l'antécédent donné) trouve **5/5**.
> Les 3 erreurs choisissent **le voisin le plus proche**, pas l'antécédent : r419 → **r428** « Il
> pleut. » (au lieu de r424 « Il mange. »), r420 → **r430** « Elle est partie. » (au lieu de r425
> « Elle dort. »), r421 → **r431** « Ils sont arrivés. » (au lieu de r426 « Ils partent. »).

## 1. Le dispositif

- **Gold** : `gold_reel.json`, paires (assertion, question) r423–r427 → r418–r422 ; les
  distracteurs r428–r432 partagent le sujet et sont **plus proches** que l'antécédent attendu.
- **Bancs** : `fidelite_lien_auto` (trouve la phrase précédente par le sujet) et
  `fidelite_contextuelle` (répond à partir de l'antécédent attendu).
- **Juge** : égalité normalisée (`juge_egal`), sans modèle.

## 2. Les résultats

| lecture | justes | taux |
|---|---:|---:|
| **lien automatique** | **2/5** | **0,40** |
| **réponse contextuelle** | **5/5** | **1,00** |

| question | attendu | trouvé | juste |
|---|---|---|---|
| r418 « Tu ne viens pas demain ? » | r423 « Tu viens demain. » | r423 | ✅ |
| r419 « Il ne mange pas ? » | r424 « Il mange. » | **r428 « Il pleut. »** | ❌ |
| r420 « Elle ne dort pas ? » | r425 « Elle dort. » | **r430 « Elle est partie. »** | ❌ |
| r421 « Ils ne partent pas ? » | r426 « Ils partent. » | **r431 « Ils sont arrivés. »** | ❌ |
| r422 « You don't come tomorrow? » | r427 « You come tomorrow. » | r427 | ✅ |

## 3. Le contrôle négatif

- Le **contextuel** (qui reçoit l'antécédent) fait **5/5** : la difficulté n'est pas la réponse,
  c'est le **choix du lien**.
- Le lien automatique fait **2/5** : il choisit la **proximité** (le voisin), pas la **cohérence
  discursive** (le même verbe, la même paire assertion/question).
- Sans distracteurs, le lien automatique fait **5/5** (mesure antérieure) : la chute est bien
  causée par les distracteurs r428–r432, pas par le banc.

## 4. Pourquoi c'est un fait, pas un bug du banc

Les distracteurs sont **légitimes** : « Il pleut. » partage le sujet « Il » avec « Il ne mange pas ? ».
Un lien qui se contente du sujet **doit** échouer ; c'est exactement ce que la ligne B13 doit
mesurer. La bonne réponse exige un critère de **paire** (assertion ↔ question du même verbe), pas
seulement le sujet.

## 5. Ce qui pourrait rendre ce résultat faux

- Le juge est une égalité de chaînes : une paraphrase juste compterait faux.
- 5 paires seulement.
- L'heuristique de sujet peut se tromper sur des pronoms ambigus.

## 6. La suite

1. **Réparer le lien** : ajouter le critère de **paire** (même verbe, assertion ↔ question) avant
   la proximité ; mesurer le gain sur les 5 paires.
2. **DRVM/native** (cadenas 3, porte 27, labyrinthe 2) — déjà mesurée.
3. Étendre les paires (10, 20) avant de conclure.

## 7. Fichiers

- [`pensee-bonne-reponse-voisin.json`](pensee-bonne-reponse-voisin.json) — la mesure et le détail.
- [`tools/tests/linguistique/miroir.py`](../tools/tests/linguistique/miroir.py) — `fidelite_lien_auto`,
  `fidelite_contextuelle`, `trouver_precedente`.
