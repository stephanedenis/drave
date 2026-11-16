# V2 — les cinq exemples rejoués : 3 blocs corrigés par les rôles normalisés, 27/27 cas conformes

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **V2** (exploitable, 21/21) ·
> **Date** : 2026-11-16 · **Verdict** : ✅
> **Cinq blocs rejoués** avec le code courant (HEAD mesuré **`2e617034`**) : **3 corrigés**,
> **2 identiques** hors enrichissement. Les corrections sont toutes la **normalisation des
> rôles** — `qualité` → `qualite`, `prédicat` → `predicat`, `groupe nominal` → `objet`. Les
> **candidats objets** sont publiés et vérifiés (**18 objets, 0 span faux**) ; la **durée** est
> documentée (`--duree`). Les **3 commandes** du démarrage sont rejouées **3/3** dans une copie
> **sans** `tools/structures` (JSON **5 899 octets**).
> **Le contrôle négatif** : [`tools/verifie_exemples.py`](../tools/verifie_exemples.py) rejoue
> **27 cas / 27 conformes, 0 écart** ; une mutation de `qualite` en `qualité` est détectée
> (**1/1**).
> **Dispositif** : [`docs/produit/exemples.md`](../docs/produit/exemples.md),
> [`docs/produit/demarrage.md`](../docs/produit/demarrage.md), `tools/drave.py` **0.1.0**,
> `jq` 1.8.2, Python 3.13.16, sans clé, sans GPU, sans réseau.
> **JSON** : [`rapport-exemples-v2.json`](rapport-exemples-v2.json).

## 1. Le verdict du rejeu

Les cinq commandes de `exemples.md` ont été relancées, puis comparées **JSON parsé** — pas le
texte — aux blocs publiés. Les sorties lisibles sont comparées ligne à ligne.

| bloc | cas | sortie du 16/11 | verdict | ce qui a bougé |
|---|---|---|---|---|
| § 1 | `g001` — « Le chat dort. » | `agent`, `predicat`, 20 étiquettes | **identique + enrichi** | `candidats_objets` ; bloc de durée |
| § 2 | `g011` — « Le livre que j'ai lu… » | 4 syntagmes, `union: true` | **corrigé** | `qualité` → `qualite` (REL longue) |
| § 3 | `r241` — « The day when we left… » | `left/VERB`, `when/CONJ` | **corrigé** | `groupe nominal` → `objet`, `qualité` → `qualite`, `prédicat` → `predicat` |
| § 4 | refus — texte vide | `stderr` + code **3** | **identique** | rien |
| § 5 | `r035` — « The film she talks about… » | `REL [9:24] → film` | **corrigé** | mêmes rôles que § 3 |

**Ce que « identique » veut dire.** Pour `g001`, les champs déjà publiés sont identiques ; le
bloc gagne `candidats_objets` et un exemple `--duree`, qui sont des **ajouts** demandés par la
tâche, pas des dérives. Pour le refus, le texte, le code et le JSON de l'API sont identiques.

## 2. Les corrections, bloc par bloc

### 2.1 `g011` — une seule valeur de rôle change

La REL courte portait déjà `role: "qualite"` ; la REL longue, qui chevauche la première, portait
la forme accentuée. Le produit publie maintenant la forme canonique :

```diff
-      "role": "qualité",
+      "role": "qualite",
```

Les spans, les cibles, `union: true`, la pragmatique et les 43 étiquettes ne bougent pas. Les
candidats objets ajoutent `livre[3:8]`, `Le livre[0:8]` et `intéressant[25:36]` selon le segment.

### 2.2 `r241` — trois rôles normalisés

Le POS anglais est celui du 14/11 (`left/VERB`, `was/AUX`, `beautiful/ADJ`, `./PONCT`) et
l'attachement `REL → day` est inchangé. Seuls les rôles changent :

```diff
-      "role": "groupe nominal",
+      "role": "objet",
...
-      "role": "qualité",
+      "role": "qualite",
...
-      "role": "prédicat",
+      "role": "predicat",
```

### 2.3 `r035` — mêmes rôles, même relative zéro

La REL `she talks about [9:24] → film` est toujours prédite ; le gold à trois spans est toujours
exact. Les trois rôles passent par la même table que `r241` (`groupe nominal` → `objet`,
`qualité` → `qualite`, `prédicat` → `predicat`). Aucun span, aucune cible ne bouge.

## 3. Les candidats objets et les rôles

Le champ historique `candidats` reste une liste de **chaînes** ; `meta.attachement.candidats`
publie les mêmes candidats en **objets** `{span, cible, source}`. Sur les quatre textes des blocs
JSON (`g001`, `g011`, `r241`, `r035`) :

| invariant | valeur | contrôle |
|---|---:|---|
| candidats objets | **18** | `tools/verifie_exemples.py` |
| spans exacts (`texte[debut:fin] == cible`) | **18/18** | le script, sur chaque objet |
| candidats non objets | **0** | le script refuse une chaîne |
| rôles publiés | **4** (`agent`, `predicat`, `objet`, `qualite`) | tous dans les **8** du vocabulaire |
| rôles hors vocabulaire | **0** | `roles_vocabulaire.ROLES` |

Quelques positions exactes : `g001` → `dort[8:12]`, `chat[3:7]` ; `g011` → `livre[3:8]`,
`intéressant[25:36]` ; `r241` → `day[4:7]`, `beautiful[25:34]` ; `r035` → `film[4:8]`,
`out[21:24]`. La cible choisie est le premier objet de la liste ; le script vérifie que chaque
`span` découpe bien la cible dans le texte.

## 4. La durée

`--duree` ajoute `cout.duree_s` ; sans le drapeau, le champ est **absent**. Le bloc du § 1 le
montre :

```json
{
  "duree_s": 0.004758,
  "octets": 13
}
```

La valeur observée au rejeu est de **4,0 à 5,8 ms** selon l'exécution. C'est une mesure locale à
l'horloge murale, pas une performance reproductible : le script vérifie la **présence** et le
**type** (`nombre >= 0`), jamais le nombre. `octets: 13` et le reste du JSON sont, eux, exacts.

## 5. Le démarrage — les trois commandes

Les trois commandes du § 3 de `demarrage.md` ont été rejouées dans une copie du code **sans**
`tools/structures`, c'est-à-dire la condition du **clone public** :

| commande | sortie | verdict |
|---|---|---|
| `drave --version` | `drave 0.1.0` | **conforme** |
| `drave analyser "Le chat dort."` | `rôle=objet`, `GV → —`, `syntagme=0.35` | **conforme** |
| `drave evaluer` | F1 **81,88 %**, attachement **88,70 %** | **conforme** |

Le § 3.4 est vérifié aussi : le JSON complet fait **5 899 octets**, l'extrait de 22 lignes et le
consommateur Python sont identiques. Le § 3.5 (`drave profils`) rend les 9 lignes publiées.
Dans le **dépôt de développement**, avec `tools/structures`, la note du § 3 est vérifiée
4/4 : `rôle=agent`, `→ chat`, F1 **79,02 %**, `ATTACHEMENT exact 99.58 %`.

La copie est un `copytree` de `tools/` moins `structures/`, `docwatch/` et `__pycache__/` ; ce
n'est **pas** un `git clone` neuf, et l'installation `pip` n'est pas re-mesurée (voir T3).

## 6. Le contrôle négatif

[`tools/verifie_exemples.py`](../tools/verifie_exemples.py) lit les deux documents, associe
chaque commande à son bloc de sortie, exécute, puis compare :

- le **JSON parsé** pour les blocs `--json` (les nombres flottants sont comparés comme des
  nombres, pas comme du texte) ;
- le **texte exact** pour les sorties lisibles ;
- `stdout`, `stderr` et le **code** pour le refus ;
- les **syntagmes** des blocs `--tagger` à l'heuristique — le tagger ne change que le POS ;
- les **trois commandes** du démarrage dans la copie sans `tools/structures` ;
- les **invariants** : candidats objets, spans exacts, rôles dans le vocabulaire, durée
  optionnelle.

Résultat : **27/27 cas conformes, 0 écart**. Le contrôle du contrôle : le mode `--mutation`
remplace `"role": "qualite"` par `"role": "qualité"` dans une copie en mémoire ; le script sort
avec **1 cas en écart** et le dit (`mutation détectée : 1 cas en écart`). Une valeur fausse ne
passe donc pas.

## 7. Ce que ce rejeu ne dit pas

1. **Le tagger n'est pas rejoué par l'API.** Les blocs du § 6 viennent d'appels réels du 15/11
   (tokens, latence, cache) ; l'API, le cache et la latence ne sont pas reproductibles à
   l'identique. Le script vérifie ce que le tagger ne change pas (les syntagmes), pas le POS
   neuronal ni le coût. Les chiffres du tagger restent ceux de
   [`rapport-tagger-option.md`](rapport-tagger-option.md).
2. **La durée n'est pas un résultat de performance.** C'est une horloge murale ; le script
   vérifie sa présence, pas sa valeur.
3. **Le démarrage n'est pas un clone réseau.** La copie sans structures reproduit la sortie du
   clone public, mais le `git clone`, le `venv` et le `pip install` ne sont pas re-mesurés ici ;
   c'est le dispositif de [`rapport-quickstart.md`](rapport-quickstart.md).
4. **Le HEAD mesuré est `2e617034`.** Le commit V2 qui porte cette fiche suit ce relevé ; les
   sorties ont été mesurées sur l'arbre courant, qui contient aussi les travaux U1–U3 non
   committés au moment du rejeu.

## 8. Ce qui est livré

- `docs/produit/exemples.md` : les cinq blocs rejoués, les candidats objets, les rôles
  normalisés et le bloc de durée.
- `tools/verifie_exemples.py` : le contrôle négatif exécutable, `--json` et `--mutation`.
- `reports/rapport-exemples-v2.md` + [`rapport-exemples-v2.json`](rapport-exemples-v2.json).
