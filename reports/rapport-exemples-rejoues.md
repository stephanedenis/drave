# J11.1 — les cinq exemples rejoués : 4 blocs sur 5 ont bougé, `r035` n'est plus un échec

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : **J11.1** · **Date** : 2026-11-14 ·
> **Verdict** : ✅
> **Cinq blocs rejoués** avec le code courant, **4 corrigés**, **1 identique** : la ponctuation
> finale entre dans le POS (`g001`, `r241`), le refus sort en **3**, et **`r035` est désormais
> prédit** — span `REL [9:24] « she talks about »` et cible `film`, exactement le gold.
> **Le chiffre.** F1 syntagmes **0,7902** ; POS **0,8625** (fermé 0,9373, ouvert 0,7918) ;
> attachement **238/238 labels** (238/239 cibles, **0,9958**). Le mandat porte encore **237/238** :
> c'est l'état d'avant `s065` (J6.2), qui a ajouté un label **sans toucher un span** — F1 inchangé.
> **Dispositif** : [`docs/produit/exemples.md`](../docs/produit/exemples.md) (les 5 blocs),
> [`tools/drave.py`](../tools/drave.py) 0.1.0, [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> `jq` ; mesure par `python3 tools/drave.py evaluer --json` sur le gold vivant (612 phrases).
> **JSON** : [`rapport-exemples-rejoues.json`](rapport-exemples-rejoues.json).

## 1. Le verdict du rejeu

Les cinq commandes de la doc ont été relancées le 14/11, puis comparées **JSON parsé** (pas le
texte) aux blocs publiés. Résultat : **5/5 blocs reproduits** après correction, **4/5 avaient
bougé**.

| bloc | cas | sortie du 14/11 | verdict | ce qui a bougé |
|---|---|---|---|---|
| § 1 | `g001` — « Le chat dort. » | 20 étiquettes, `./PONCT` | **corrigé** | 19 → 20 étiquettes ; POS `0,92` → `0,95` |
| § 2 | `g011` — « Le livre que j'ai lu… » | identique champ pour champ | **inchangé** | rien dans le filtre ; v2 ajoute `meta.partition` |
| § 3 | `r241` — « The day when we left… » | `left/VERB` (0,85) | **corrigé** | `left` était `NOUN` (0,3) ; `./PONCT` ajouté |
| § 4 | refus — texte vide | `stderr` + code **3** | **corrigé** | code **1 → 3** ; `--json` rend l'annotation |
| § 5 | `r035` — « The film she talks about… » | `REL [9:24] → film` | **corrigé** | l'ancien échec connu est **prédit** |

**Ce que le rejeu ne dit pas.** Il ne mesure pas la qualité du produit : il vérifie que la **doc
dit ce que le code fait**. Les chiffres de qualité (F1, POS, attachement) viennent de `evaluer`,
pas de ces cinq phrases.

## 2. Les corrections, bloc par bloc

### 2.1 `g001` — la ponctuation entre dans le POS

La sortie lisible passe de 19 à **20 étiquettes** : le point final est désormais un token `PONCT`.

```
- POS  Le/DET chat/NOUN dort/VERB
+ POS  Le/DET chat/NOUN dort/VERB ./PONCT
- COUVERTURE … pos=0.92 …
+ COUVERTURE … pos=0.95 …
```

Dans le JSON, un quatrième objet POS apparaît : `{"valeur": ".", "type": "PONCT", "debut": 12,
"fin": 13, "confiance": 0.95, "ouvert": false}`. Les deux syntagmes, la phrase et la pragmatique
sont inchangés ; les **2 unités** et **61,5 %** du texte aussi.

### 2.2 `g011` — identique, mais v2 publie la partition

Le filtre de la doc ne sélectionne pas `meta.partition` : à ce niveau, la sortie est **identique**
champ pour champ. Le JSON **complet** est passé en v2 sur ce cas de chevauchement : les trois
segments du groupe 0 portent `meta.partition` (`membres: 3` ; rang 1 = REL longue, rang 2 = GV,
rang 3 = REL courte) et `meta.alternative` avec les deux autres. La doc le dit maintenant au § 2.

C'est le seul bloc que le rejeu n'a pas eu à corriger.

### 2.3 `r241` — `left` n'est plus un nom

Le POS anglais a progressé : `left` était `NOUN` (0,3), il est **`VERB`** (0,85). Le point final
sort aussi en `PONCT` (0,95). Le reste du bloc — `when/CONJ`, `was/AUX`, `beautiful/ADJ`, les trois
syntagmes et l'attachement `REL → day` — est inchangé.

La leçon de la doc (« une réussite d'attachement peut coexister avec des erreurs de POS ») tient
toujours, mais l'exemple a changé : le POS n'est plus faux sur `left`. Les chiffres cités sont
recalés : POS **0,8625**, ouvert **0,7918**, attachement anglais **87/87 labels** (88 cibles,
`g017` manquante).

### 2.4 Le refus — le contrat est implémenté

Sans `--json`, le CLI écrit toujours le message sur `stderr`, mais sort **3** (et non 1) :

```
drave: refus d'analyse : vide (le texte doit contenir au moins une lettre ou un chiffre)
exit=3
```

Avec `--json`, il écrit sur `stdout` une annotation de refus (`schema: "drave.annotation"`,
`version: 2`, `refus: "vide"`, `etiquettes: []`) et sort **3**. Le contrat « code 3 + JSON » est
donc tenu ; la doc ne peut plus dire qu'il ne l'est pas. L'API `bloc_linguistique.py` rend le même
état (`langue: und`, `script: Zyyy`, `refus: "vide"`, 0 étiquette).

### 2.5 `r035` — l'ancien échec est devenu le cas réussi

C'est le changement de fond du rejeu. La règle de **relative zéro** (J1.1, `relative_zero`) rend
exactement le gold :

| avant (doc du 06/11) | après (14/11) |
|---|---|
| `GN « The film she » [0:12] → talks` | `GN « The film » [0:8] → out` |
| `GV « talks » [13:18] → null` | `REL « she talks about » [9:24] → film` |
| `GV « about is out » [19:31] → null` | `GV « is out » [25:31] → null` |

Le gold attend `REL [9:24] « she talks about » → film` : le span **et** la cible sont justes.
Conséquence sur les chiffres : l'exactitude d'attachement est **238/238 labels = 1,0000**, mais
elle reste **conditionnelle aux spans prédits** ; la couverture est **238/239 = 0,9958**. Le seul
span du gold encore manquant qui porte une cible est **`g017`** (`SUB [9:28] « that she would
come »`, étendue à `[9:38]` par absorption de `yesterday`) ; la règle qui le corrigerait a été
rejetée (J6.1, test −0,0028 ; [fiche](rapport-g017.md)).

La doc ne présente donc plus `r035` comme un échec : elle raconte le cas autrefois manqué et
nomme `g017` comme échec courant.

## 3. La mesure courante

Gold **vivant** (hand + reel + synthétique) : **612 phrases**, **3 179 tokens**, **239 cibles**
d'attachement.

| mesure | valeur | lecture |
|---|---:|---|
| POS (tous) | **0,8625** | inchangée depuis `r035` |
| POS fermé / ouvert | **0,9373** / **0,7918** | l'ouvert reste le point faible |
| F1 syntagmes | **0,7902** | précision 0,7860 · rappel 0,7944 |
| tp / fp / fn | **1 480 / 403 / 383** | union |
| tête (F1) | **0,9029** | |
| attachement exact / labels | **238/238** | 1,0000 conditionnel |
| couverture (cibles) | **238/239 = 0,9958** | `g017` manquante |
| français | **151/151 labels** | 151 cibles |
| anglais | **87/87 labels** | 88 cibles (`g017`) |

**Le point de mandat.** Le mandat écrit « 237/238 ». C'est l'état d'avant J6.2 : `s065` a corrigé
une **cible** sans toucher un span, donc **238/238 labels** et **F1 0,7902 inchangé**. Écrire
237/238 aujourd'hui serait un chiffre périmé de plus.

## 4. Contrôle négatif

**Le dispositif.** Un comparateur lit les blocs ```json de la doc, garde les cinq qui ont une clé
`langue`, relance les commandes et compare les **objets JSON** (pas le texte, donc l'ordre des
clés et l'indentation ne comptent pas).

| essai | résultat |
|---|---|
| doc réelle | **5/5** blocs identiques, code 0 |
| doc mutée : `left/VERB` → `left/NOUN` (exemple 3) | **4/5**, code 1 ; écart `.pos[4].type: 'NOUN' != 'VERB'` |

La mutation est un **drift d'un seul token** : si le comparateur recopiait la doc au lieu de
rejouer, il ne verrait rien. Il le voit. C'est le contrôle qui manque à un simple « ça a l'air
bon ».

## 5. Ce qui pourrait rendre ce rapport faux

1. **Le rejeu est daté.** Les sorties valent pour le code de
   `03ecee413cb05cf906d623765443d98d317e7f59` et le CLI 0.1.0 ; le HEAD du rapport est
   `a6808c5edf741ea59d45602fdfeee0916488beaf` (commit superviseur, sans changement produit) ;
   tout changement de code, de lexique ou de ponctuation les déplace.
2. **Cinq exemples ne sont pas un échantillon.** Ils vérifient la doc, pas la qualité. Les
   chiffres de § 3 viennent de `evaluer` sur 612 phrases et ne sont pas indépendants des règles
   écrites sur ce gold (in-sample).
3. **Le gold est une convention.** `g017` reste un arbitrage non tranché (adverbe final) ; si le
   gold change, la couverture change sans que le code bouge.
4. **La comparaison est partielle.** Elle porte sur les champs que les filtres de la doc
   sélectionnent, pas sur `trace`, `cout` ni `meta.partition`/`alternative` (vérifiés à la main
   pour `g011`).
5. **Le mandat est en retard d'un label.** 237/238 est l'état d'avant `s065` ; le chiffre courant
   est 238/238 labels (238/239 cibles). Un rapport qui recopie le mandat se trompe.

## 6. Fichiers

- [`docs/produit/exemples.md`](../docs/produit/exemples.md) — les 5 blocs, l'en-tête daté du
  14/11, le § 5 réécrit et le § 6.3 recalé.
- [`rapport-exemples-rejoues.json`](rapport-exemples-rejoues.json) — les 5 sorties, les écarts,
  la mesure et le contrôle négatif.
- [`tools/drave.py`](../tools/drave.py) · [`bloc_linguistique.py`](../tools/bloc_linguistique.py) —
  le code rejoué.
- [`rapport-r035.md`](rapport-r035.md) · [`rapport-s065.md`](rapport-s065.md) ·
  [`rapport-g017.md`](rapport-g017.md) — l'histoire des trois cas cités.

**La suite.** **J11.2** ajoute `evaluer --par-langue` et le documente ; **J11.3** re-mesure les
50 textes libres ; **J11.4** documente le schéma v2.
