# Audit de reproductibilité — l'attachement du bloc linguistique (B13)

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Verdict** : ✅ **reproduit — 14/14 valeurs, écart 0** ; ⚠️ **réserve documentaire** :
> **3 des 5 JSON sont des instantanés antérieurs**, reproduits à leur commit mais pas à
> l'état courant. L'audit n'a modifié aucun fichier existant et n'a fait aucun commit.

> **Dispositif** : depuis la racine, `sys.path.insert(0, '.')` ;
> `from tools.bloc_linguistique import Heuristique` ;
> `from tools.tests.linguistique.evaluer_gold import charger, evaluer_bloc` ;
> `evaluer_bloc("heuristique", Heuristique(), charger())` pour l'attachement ; pour les spans,
> même boucle que `T166` : chaque `segment` du gold est comparé aux étiquettes de niveau
> `syntagme` par `(type, debut, fin)`. Mesure rejouée sur `s/v7`, commit **`e1171032`**,
> `bloc_linguistique.py` sha256 **`d9c9d559…`**, `evaluer_gold.py` sha256 **`dbbcfe90…`**,
> gold inchangé (612 phrases : 20 `hand` + 432 `reel` + 160 synthétiques). Durée : 0,45–0,55 s.
> Les cinq JSON sont lus dans leur version du commit **`e1171032`** ; la note de concurrence
> du § 3 dit ce qui a bougé dans le worktree pendant l'audit.

## 1. Verdict

Les **14 nombres publiés** le 2026-11-05 reproduisent **exactement**, sans arrondi et sans
« correction » : cibles 239, labels 145, top1 126, top-k (sous-chaîne) 134, exact 123,
top-k strict 88, couverture 0,6067, verbes 63 (60 justes), noms 82 (63 justes), spans perdus
48 REL / 33 SUB / 13 GP.

La réserve est **documentaire, pas métrologique** : `pensee-conventions.json` (commit
`f70a1b2a`), `pensee-attachement-cible.json` (`23853cb7`) et `pensee-spans.json`
(`d400e188` / `13e8bb2d`) décrivent des états **antérieurs**. Rejoués à leur commit, ces
fichiers sont justes — ils ne sont simplement plus l'état courant. `pensee-topk-strict.json`
(`e223a98d`) et `pensee-echecs-cible.json` (`a048cb83`) sont, eux, **identiques à l'état
courant**. Le point le plus net : dans sa version **committée**, `pensee-spans.json` publie
**12 GP / 93 spans** dans son bloc `spans`, alors que le chiffre audité est **13 GP / 94** —
c'est l'état courant (et le bloc « avant » du même JSON), pas son bloc « après ».

## 2. Tableau mesuré / publié / écart

| mesure | mesuré | publié | écart |
|---|---:|---:|---:|
| cibles (segments gold avec cible) | **239** | 239 | **0** |
| labels (segments au bon span) | **145** | 145 | **0** |
| top1 | **126** | 126 | **0** |
| top-k (sous-chaîne) | **134** | 134 | **0** |
| exact | **123** | 123 | **0** |
| top-k strict (égalité exacte) | **88** | 88 | **0** |
| couverture (labels / cibles) | **0,6067** | 0,6067 | **0** |
| cibles verbes | **63** | 63 | **0** |
| justes verbes | **60** | 60 | **0** |
| cibles noms | **82** | 82 | **0** |
| justes noms | **63** | 63 | **0** |
| spans perdus REL | **48** | 48 | **0** |
| spans perdus SUB | **33** | 33 | **0** |
| spans perdus GP | **13** | 13 | **0** |

Taux dérivés (dénominateurs : 145 labels, 239 cibles) — la colonne « dans les JSON » n'est
**pas** l'état courant, elle indique le chiffre du fichier et son état :

| mesure | mesuré | dans les JSON |
|---|---:|---:|
| top1 / labels | 0,8690 | 0,8356 (`attachement-cible`, apres, 146) |
| top1 / cibles | 0,5272 | 0,5105 (`attachement-cible`, rendement) |
| top-k / labels | 0,9241 | 0,9241 (`topk-strict`, 145) |
| top-k / cibles | 0,5607 | 0,5607 (`topk-strict`) |
| exact / labels | 0,8483 | 0,8082 (`attachement-cible`, apres) ; 0,8483 (`topk-strict`, note) |
| exact / cibles | 0,5146 | 0,4937 (`attachement-cible`, rendement) |
| top-k strict / labels | 0,6069 | 0,6069 (`topk-strict`) |
| top-k strict / cibles | 0,3682 | 0,3682 (`topk-strict`) |
| verbe (60/63) | 0,9524 | 0,9412 (48/51, `attachement-cible`) |
| nom (63/82) | 0,7683 | 0,7368 (70/95, `attachement-cible`) |
| F1 syntagmes | 0,2862 | 0,2864 (`spans`, avant) ; 0,2869 (`spans`, après) |

Le F1 courant vient de 488 tp / 1059 fp / 1375 fn (précision 0,3154, rappel 0,2619).

## 3. Confrontation aux cinq JSON

| JSON | commit | valeurs du fichier | état courant | verdict |
|---|---|---|---|---|
| `pensee-conventions.json` | `f70a1b2a` | labels 146 ; verbes 37/51 (0,7255) ; noms 57/95 (0,6000) ; tout 94 (0,6438) | 145 ; 60/63 (0,9524) ; 63/82 (0,7683) ; 123 (0,8483) | instantané antérieur ; **reproduit à son commit** |
| `pensee-attachement-cible.json` | `23853cb7` | labels 146 ; top1 122 ; exact 118 ; exact_span 0,8082 ; top1_span 0,8356 ; verbes 48/51 ; noms 70/95 | 145 ; 126 ; 123 ; 0,8483 ; 0,8690 ; 60/63 ; 63/82 | instantané antérieur ; **reproduit à son commit** |
| `pensee-topk-strict.json` | `e223a98d` | 145 ; 134 (0,9241 / 0,5607) ; 88 (0,6069 / 0,3682) | identique | **reproduit** |
| `pensee-spans.json` | `d400e188` / `13e8bb2d` | après : 146 ; 0,6109 ; 0,2869 ; 93 ; REL 48 / SUB 33 / **GP 12** ; avant : 145 ; 0,6067 ; 0,2864 ; 94 ; cible 13 | 145 ; 0,6067 ; 0,2862 ; **94** ; REL 48 / SUB 33 / **GP 13** ; cible 11 | les deux blocs **historiques** reproduisent ; l'état courant est le bloc `courant` ajouté depuis (hors audit) |
| `pensee-echecs-cible.json` | `a048cb83` | 145 ; 123 ; 22 ; 11 hors + 11 mal classés ; GP 14/0/10, SUB 5/3/1, REL 0/0/0 | identique | **reproduit** |

Le détail des spans, qui concentre l'écart :

| | avant (`d400e188`) | après (`13e8bb2d`) | **courant** |
|---|---:|---:|---:|
| labels | 145 | 146 | **145** |
| couverture | 0,6067 | 0,6109 | **0,6067** |
| F1 syntagmes | 0,2864 | 0,2869 | **0,2862** |
| spans perdus | 94 | 93 | **94** |
| REL / SUB / GP | 48 / 33 / 13 | 48 / 33 / 12 | **48 / 33 / 13** |
| catégories (aucun / plus large / plus étroit / coupe) | 65 / 25 / 3 / 1 | 65 / 24 / 3 / 1 | **65 / 24 / 4 / 1** |
| cible absente des candidats | 13 | 14 | **11** |

**Version comparée et concurrence** : les valeurs ci-dessus sont celles des blobs du commit
`e1171032`. Pendant l'audit, un **autre agent** a ajouté à `pensee-spans.json` un bloc
`courant` (145 / 0,6067 / 0,2862 / 94 / REL 48, SUB 33, GP 13 / 65-24-4-1) et corrigé le
titre de `rapport-pensee-spans.md` ; cet audit n'a touché à **aucun** des deux. Le bloc ajouté
reprend exactement les valeurs mesurées ici — il ne change ni la mesure ni le verdict, il
matérialise l'état courant dans le JSON.

**Ce que ça dit** :

- Le correctif GP de `13e8bb2d` gagne bien un span (146 labels, **GP 12**, F1 0,2869) ;
  l'attachement ciblé de `23853cb7` porte ensuite l'exact à 118 (sur 146 labels). Puis le
  **lexique élargi** `a408a909` (10:39) repasse à **145 labels / GP 13 / F1 0,2862** tout en
  faisant monter l'exact de 118 à **123**. L'état courant est stable depuis `a048cb83`.
- Les deux états de `pensee-spans.json` sont donc justes **à leurs commits**, mais sa version
  **committée** ne contient **que** le couple avant/après : aucun des deux n'est l'état courant.
- Dans sa version **committée** (`e1171032`), le titre de la fiche `rapport-pensee-spans.md` —
  « les 94 spans : 48 REL, 33 SUB, 12 GP » — mélangeait le total **avant** (94) et la
  ventilation **après** (48 + 33 + 12 = 93) : incohérence de rédaction, pas de mesure. Le
  tableau du corps disait bien 93. Le titre a été corrigé depuis par l'ajout concurrent.
- Le bloc `categories` de `pensee-spans.json` (65 / 25 / 3 / 1) est la lecture **avant** : il
  somme 94, alors que le bloc `apres` du même fichier annonce 93 spans.
- `pensee-echecs-cible.json` est cohérent : la colonne `hors` est un **sous-ensemble** des
  échecs (GP 10 et SUB 1), pas une ligne supplémentaire ; 14 + 0 + 5 + 3 = 22 échecs.

## 4. Contrôle négatif

Le bon score n'est pas un artefact de vocabulaire. Trois baselines, graine `20261105`,
1 000 tirages :

| contrôle | résultat | lecture |
|---|---:|---|
| **exact observé** | **123/145 = 0,8483** | la règle |
| permutation des cibles gold | 1,62/145 = **0,0112** (min 0, max 7, σ 1,27) | 76× l'observé ; observé hors distribution |
| candidat tiré au hasard parmi les candidats produits | 39,75/145 = **0,2742** (min 27, max 52, σ 4,53) | 3,1× l'observé ; observé hors distribution |
| contrôle du harnais (`attachement_hasard`) | 1/239 = **0,0042** | tirage d'une cible gold au hasard |

Le contrôle « candidat aléatoire » est le plus dur : la liste de candidats seule donne déjà
27,4 %, la règle fait 84,8 % — soit +57 points. Mais l'exact et le top-k strict ne mesurent
pas le même objet : **82** labels sont exacts **et** dans la liste stricte, **41** exacts ont
une cible **absente** de cette liste, et **6** cibles présentes sont mal choisies. L'écart
123 − 88 = 35 n'est donc pas « 35 réponses trouvées hors liste » ; c'est 41 − 6. Le top-k
strict (60,7 %) reste la mesure de la **couverture de la liste**, pas un plafond de l'exact.

## 5. Limites

- **Trois JSON sur cinq sont des instantanés antérieurs** (commits ci-dessus) : ils ne doivent
  pas être relus comme l'état courant. Ils n'ont pas été modifiés par cet audit (consigne) ;
  le présent audit et les deux JSON courants (`topk-strict`, `echecs-cible`) font foi.
- **Concurrence** : un autre agent a ajouté un bloc `courant` à `pensee-spans.json` et corrigé
  `rapport-pensee-spans.md` pendant l'audit ; ces ajouts reprennent les valeurs mesurées
  (145 / 0,6067 / 0,2862 / 94 / 48-33-13 / 65-24-4-1) et ne sont pas de cet audit. La
  comparaison ci-dessus reste celle des blobs du commit `e1171032`.
- **`pensee-spans.json` publie 12 GP / 93 spans**, pas 13 / 94 : le chiffre audité est
  l'état courant, pas le bloc `apres` du fichier. La fiche `rapport-pensee-spans.md` porte en
  plus une incohérence de titre (94 avec une ventilation à 93).
- **Catégories de spans** : la règle retenue est explicite — `aucun` = aucun segment du même
  type ne recouvre le gold ; `coupe` = au moins **deux** segments le recouvrent ; `plus large`
  = un seul, qui contient le gold ; `plus étroit` = un seul, contenu dans le gold. Elle
  reproduit exactement le 65 / 25 / 3 / 1 de l'état « avant » ; le courant donne 65 / 24 / 4 / 1.
- **Dépendance S** : la segmentation vient du sous-module `tools/structures` au commit
  `523d8c1`. Son fichier de données modifié (`donnees/paragraphes-validations.jsonl`) n'est
  lu que par `serveur.py`, pas par `generateur.analyser` : il n'affecte pas cette mesure.
- **Gold vivant** : 612 phrases ; `gold_gele` (602) n'est pas utilisé ici. Le chiffre « gold
  612 » des fiches est donc bien celui de `charger()`.
- **Portes non rejouées** : les 169/169 … 176/176 des fiches ne sont pas audités ; l'audit
  porte sur la mesure d'attachement, pas sur le registre de non-régression.
- **HEAD a avancé pendant l'audit** (commits de pilotage) ; l'état mesuré est épinglé par le
  commit `e1171032` et les sha256 du dispositif. Une mesure identique a été obtenue deux fois
  (seule la durée change).
- **Dénominateurs** : 145 labels (segments au bon span) et 239 cibles (segments gold avec
  cible) ne sont pas interchangeables ; les deux taux sont publiés séparément, jamais fondus.

## 6. Fichiers

- [`../tools/tests/linguistique/evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py)
  — `charger`, `evaluer_bloc`, `_seg`, `_est_verbe`.
- [`../tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) — `Heuristique`,
  `_tete_nom`, `_verbe_dans`, `_est_verbe`.
- [`../tools/structures/generateur.py`](../tools/structures/generateur.py) — le générateur S
  (sous-module `523d8c1`).
- [`pensee-attachement-cible.json`](pensee-attachement-cible.json) ·
  [`pensee-conventions.json`](pensee-conventions.json) ·
  [`pensee-topk-strict.json`](pensee-topk-strict.json) ·
  [`pensee-spans.json`](pensee-spans.json) ·
  [`pensee-echecs-cible.json`](pensee-echecs-cible.json) — les cinq JSON confrontés,
  **version du commit `e1171032`**, non modifiés par cet audit (le bloc `courant` ajouté
  ensuite à `pensee-spans.json` vient d'un autre agent).
- [`pensee-audit-attachement.json`](pensee-audit-attachement.json) — les mêmes chiffres,
  structurés, avec les rejeux des commits historiques.

**L'audit n'a modifié aucun fichier existant et n'a fait aucun commit** : il produit deux
fichiers neufs, conformément à la consigne.
