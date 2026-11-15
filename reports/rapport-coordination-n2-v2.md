# N2 — la commande validée : le canal avec RoPE, et le témoin 3,09 qui ne doit pas bouger

> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-15 · **HEAD mesuré** :
> `5891ef8a` · **Verdict** : la mesure **2,79** est celle du couple **RoPE + canal**, rejouée
> **2,9726 / 2,8988 / 2,8443 / 2,7856** de 128 à 1 024 octets. **`--rope` sans canal rend
> 40,0658** à 128 et **65,7898** à 1 024 : c'est la commande à ne pas utiliser. La commande du
> mandat, `eval_longueurs.py --rope --canal-dir <dir>`, **n'existe pas telle quelle** :
> `--canal-dir` est le drapeau du correctif `eval_n2_propre.py` (validé en copie `/tmp`), et
> `eval_longueurs.py` fournit le canal par `--val <dir>`. Le test `porte-n2.sh` proposé doit tenir
> **deux** invariants : la porte RoPE + canal à **2,7856**, et le témoin absolu N2.h à **3,09**
> (mesuré **3,0971** en validation, **3,2098** en test). **Aucun fichier de `tools/n2/` ni de
> `work/n2ac/` n'a été modifié.**

**En trois lignes.** (1) La commande validée, exécutable aujourd'hui, est
`work/n2ac/eval_longueurs.py --rope --val <dir>` — le `--val` **est** le canal ; (2) le correctif
`tools/eval_n2_propre.py --rope --canal-dir <dir>` donne les mêmes chiffres mais n'est pas encore
dans le dépôt, et `--rope` **sans** canal donne **40,07** ; (3) `porte-n2.sh` doit vérifier que
**3,09 reste 3,09** avant de vérifier 2,79 — sinon le correctif peut déplacer les deux mètres sans
qu'on le voie.

## Ce que cette fiche est, et n'est pas

- **Est** : la suite de [`rapport-coordination-n2.md`](rapport-coordination-n2.md). Elle lève une
  **ambiguïté de commande** que la v1 laissait ouverte (deux mètres, deux drapeaux), rejoue les
  chiffres au HEAD courant, et propose le test de non-régression.
- **N'est pas** : un patch, ni un commit de N2. `tools/eval_n2_propre.py`, `work/n2ac/` et
  `tools/n2/` (absent de l'arbre) sont **lus, non modifiés**. La session N2 reste seule à écrire
  dans son territoire.
- **Public** : la session N2 et toute session qui doit **mesurer** la porte sans la casser.

## 1. Ce que la v2 corrige — une commande hybride

La v1 disait deux choses justes, dans deux sections différentes :

| v1 | commande | ce que c'est |
|---|---|---|
| § 4.A | `work/n2ac/eval_longueurs.py --rope --val data/corpus_propre` | le mètre **existant** ; le canal vient de `val.canal` |
| § 3.2 / 4.B | `tools/eval_n2_propre.py --rope --canal-dir data/corpus_propre` | le **correctif proposé**, validé en copie `/tmp` |

Le plan de la tâche C1 a fusionné les deux en
`python3 work/n2ac/eval_longueurs.py --rope --canal-dir <dir>`. Cette forme **ne tourne pas** :
`eval_longueurs.py` n'a pas de `--canal-dir` (vérifié le 15/11, code de sortie **2**) :

```text
eval_longueurs.py: error: unrecognized arguments: --canal-dir data/corpus_propre
```

Le fond du message reste vrai — **il faut le canal** — mais la forme est fausse : ce n'est pas le
même outil, ni le même drapeau. La v2 donne donc les commandes **exactes**, avec le nom du fichier
qui les accepte.

## 2. Les trois commandes

### A. La commande validée, exécutable aujourd'hui — le chiffre 2,79

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python work/n2ac/eval_longueurs.py \
  work/n2ac/propre512-8k.pt \
  --rope --longueurs 128,256,512,1024 --val data/corpus_propre
```

Sortie rejouée le **15/11 à 02 h 09 HNE**, à l'identique :

```text
L128 : 2.9726
L256 : 2.8988
L512 : 2.8443
L1024 : 2.7856
```

**Le point clé** : ici `--val data/corpus_propre` **est** le canal. `eval_longueurs.py` lit
toujours `val.canal` (ligne 44 du script) ; il n'y a pas de mode « sans canal ». C'est pourquoi
`--rope` **avec le bon `--val`** ne rend pas 40,07 : le canal est fourni. La formule « `--rope`
seul » ne désigne donc pas ce mètre — elle désigne le correctif de `eval_n2_propre.py` (§ 2.C).

### B. Le correctif validé, mais pas encore dans le dépôt — même 2,79

La copie de travail de la v1, `/tmp/eval_n2_propre_rope.py`, ajoute `--rope` **et**
`--canal-dir` à `tools/eval_n2_propre.py`. Rejouée le 15/11 :

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python /tmp/eval_n2_propre_rope.py \
  work/n2ac/propre512-8k.pt \
  --rope --canal-dir data/corpus_propre --longueurs 128,256,512,1024
```

```json
{"fichier": "propre512-8k.pt", "params": 34301224,
 "val": 2.9726, "test": 3.0807,
 "longueurs": {"128": 2.9726, "256": 2.8988, "512": 2.8443, "1024": 2.7856},
 "permute": 1673.4162}
```

C'est **la** forme `--rope --canal-dir <dir>` du mandat : elle est correcte, mais elle appartient à
`tools/eval_n2_propre.py`, pas à `work/n2ac/eval_longueurs.py`. Pour la rendre durable, la session
N2 doit appliquer le diff de la v1 (§ 3 de
[`rapport-coordination-n2.md`](rapport-coordination-n2.md)) — **hors du périmètre de C1**.

### C. La commande à ne PAS utiliser — `--rope` sans canal : 40,07

```bash
# copie /tmp, le drapeau --rope est fourni mais PAS --canal-dir
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python /tmp/eval_n2_propre_rope.py \
  work/n2ac/propre512-8k.pt --rope --longueurs 128,256,512,1024
```

```text
L128  sans canal : 40.0658
L256  sans canal : 49.5308
L512  sans canal : 59.8126
L1024 sans canal : 65.7898
```

C'est le piège : `--rope` corrige l'**architecture**, pas l'**entrée manquante**. Le checkpoint de la
porte a été entraîné avec `--canal data/corpus_propre/train.canal`
(`work/n2ac/chaine_porte.sh`) ; sans lui, la perplexité est **13,5 fois** pire à 128 et **23,6 fois**
pire à 1 024 que la valeur avec canal.

Pour mémoire, le mètre actuel **sans** `--rope` (architecture absolue) rend **8,0225** à 128 et
**38,5288** à 1 024 : les deux modes faux sont **au-dessus** de la bonne réponse (2,79), et ni l'un
ni l'autre n'est la porte.

## 3. Les chiffres rejoués au HEAD `5891ef8a`

Checkpoint de la porte : `work/n2ac/propre512-8k.pt`, **34 301 224** paramètres, `window = 512`,
`positions = rope`, sha256 `37c5673b3d51f6f871c4391b97015b401f73c842d04d4a05f78a70c2b264eefc`.
Validation `data/corpus_propre/val.txt`, fenêtres Van der Corput dans les chunks de 8 192,
8 lots × 16 fenêtres ; tout est déterministe (2,7856 deux fois).

### 3.1 La courbe de longueur — trois mètres, un seul juste

| mètre | canal | 128 | 256 | 512 | 1 024 |
|---|---|---:|---:|---:|---:|
| `eval_longueurs.py --rope --val <dir>` | **oui** (`val.canal`) | **2,9726** | **2,8988** | **2,8443** | **2,7856** |
| `eval_n2_propre.py --rope --canal-dir <dir>` (copie `/tmp`) | **oui** | **2,9726** | **2,8988** | **2,8443** | **2,7856** |
| `eval_n2_propre.py --rope` seul (copie `/tmp`) | **non** | 40,0658 | 49,5308 | 59,8126 | 65,7898 |
| `eval_n2_propre.py` sans `--rope` (absolu) | non | 8,0225 | 8,9710 | 11,3357 | 38,5288 |

Les deux premières lignes sont **identiques au chiffre près**. La troisième **monte** avec la
longueur (40 → 66) : c'est la signature d'une entrée manquante, pas d'un modèle qui extrapole. La
quatrième monte aussi (8 → 38,5) : l'architecture absolue n'a pas de position relative.

### 3.2 Le test — la mesure honnête

Split temporaire (`test.txt` → `val.txt`, `test.canal` → `val.canal`), même mètre :

```bash
mkdir -p /tmp/c1-propre-test
cp data/corpus_propre/test.txt  /tmp/c1-propre-test/val.txt
cp data/corpus_propre/test.canal /tmp/c1-propre-test/val.canal
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python work/n2ac/eval_longueurs.py \
  work/n2ac/propre512-8k.pt --rope --longueurs 128,512,1024 --val /tmp/c1-propre-test
```

| longueur | test |
|---:|---:|
| 128 | 3,0649 |
| 512 | 2,8875 |
| **1 024** | **2,8566** |
| seuil | 2,5000 |
| **manque** | **0,3566** |

La validation manque la porte de **0,2856** ; le test, de **0,3566**. Le chiffre 2,79 est le
**meilleur des quatre longueurs en validation**, choisi après coup : 2,8566 est la mesure honnête.
La porte **< 2,5 n'est pas atteinte**, et cette fiche ne prétend pas le contraire.

### 3.3 Le témoin absolu — la porte à 3,09

`work/n2h/A-propre-g1.pt` (11 816 136 paramètres, positions absolues, **sans** canal), mètre
`tools/eval_n2_propre.py` (non patché) :

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 \
  ~/gpu-env/bin/python tools/eval_n2_propre.py work/n2h/A-propre-g1.pt --longueurs
```

```json
{"fichier": "A-propre-g1.pt", "params": 11816136,
 "val": 3.0971, "test": 3.2098, "permute": 1356.6433,
 "longueurs": {"129": 3.1334, "192": 8.7137, "256": 14.4554, "384": 24.8061, "512": 34.0535}}
```

**3,0971** est dans la classe de la chaîne honnête N2.h publiée (**3,0904** val / **3,1960** test,
[`rapport-n2-porte-propre.md`](rapport-n2-porte-propre.md)) : c'est le **3,09** à ne pas casser.
Le même checkpoint **avec** canal rend 10,99 ([`rapport-coordination-n2.md`](rapport-coordination-n2.md)) :
le canal ne s'ajoute pas à un modèle qui ne l'a pas appris ; de même, RoPE ne s'ajoute pas à un
modèle absolu.

## 4. Le test de non-régression proposé — `tools/porte-n2.sh`

**Statut** : **proposée, non écrite**. L'écrire est un acte N2 (création d'une porte, entrée dans
`tools/toutes-les-portes.sh`, compteur 85 → 86) ; C1 documente le contrat, N2 l'implémente.

### 4.1 Les deux invariants, dans cet ordre

| # | invariant | commande | attendu | tolérance |
|---|---|---|---|---|
| **A** | **la porte à 3,09 reste à 3,09** | `tools/eval_n2_propre.py work/n2h/A-propre-g1.pt` | `val = 3,0971`, `test = 3,2098` | ± 0,01 |
| **B** | la porte RoPE + canal vaut 2,79 | `work/n2ac/eval_longueurs.py work/n2ac/propre512-8k.pt --rope --val data/corpus_propre --longueurs 128,256,512,1024` | `2,9726 / 2,8988 / 2,8443 / 2,7856` | ± 0,01 |
| **B'** | la courbe descend | `L1024 < L128 − 0,15` | − 0,187 | — |
| **B''** | le test 1 024 | split `test` → `val`, même mètre | `2,8566` | ± 0,01 |
| **C** | contrôle négatif | validation permutée (VDC), canal inchangé, 1 024 | `1 692,39` (v1) / `1 673,42` à 128 (patché) | > 100 |
| **D** | statut absolu | `2,7856 − 2,5` ; `2,8566 − 2,5` | manque **0,2856** / **0,3566** | imprimé |

**Pourquoi A d'abord.** Si le correctif `--rope`/`--canal-dir` est appliqué sans garde-fou, il peut
faire basculer **tous** les checkpoints dans le chemin RoPE. Le témoin absolu `A-propre-g1.pt`
rendrait alors un chiffre de la classe 40, pas 3,09 — et personne ne le verrait si la porte ne
vérifie que 2,79. **La non-régression de N2 n'est pas « 2,79 est reproductible » ; c'est « 3,09
reste 3,09 ET 2,79 reste 2,79 ».** Les deux bras mesurent deux architectures différentes : les
confondre serait un faux progrès.

### 4.2 Le contrat d'exécution

```text
tools/porte-n2.sh
  entrée   : aucun argument ; GPU ; work/ et data/ présents
  sortie 0 : A et B (et B' si activé) tenus ; D imprimé
  sortie 1 : un invariant est violé (dérive du mètre ou du checkpoint)
  sortie 2 : artefact ou GPU absent (comme porte-budget / porte-adaptateur-sortie)
  temps    : ~40 s pour A + B (deux chargements), ~55 s avec B'' et C
  JAMAIS 0 sur le seuil 2,5 : la porte scientifique reste rouge (manque 0,2856/0,3566) ;
           la non-régression n'est pas le succès.
```

Le script doit imprimer les deux lignes, même quand tout va bien :

```text
N2 temoin absolu : val 3.0971 test 3.2098  [3,09 attendu]      OK
N2 porte RoPE+canal : L1024 2.7856          [2,79 attendu]      OK
N2 statut absolu : 2.7856 - 2.5 = +0.2856 (val) / +0.3566 (test)  ROUGE (seuil 2,5)
```

**Ce qu'elle ne doit pas faire** : réentraîner, télécharger, toucher `en-cours`/roadmap, mesurer le
grand corpus à la place du corpus propre, utiliser `eval_n2_propre.py` **sans** `--rope` sur un
checkpoint RoPE, ou appeler `eval_longueurs.py` avec `--canal-dir` (le drapeau n'existe pas).
**Dépendances** : `~/gpu-env/bin/python` (torch CUDA), `work/n2ac/{eval_longueurs.py,rope_model.py}`,
`work/n2j/evalue_canal.py`, `work/n2ac/propre512-8k.pt`, `work/n2h/A-propre-g1.pt`,
`data/corpus_propre/{val,test}.{txt,canal}` — tous **non suivis** (`work/`, `data/` gitignorés).
La porte est donc **locale à Hauru**, comme le mètre ; c'est dit dans son en-tête.

## 5. La mise à jour de la ligne N2 de `en-cours`

La ligne **N2 — en pause** de [`docs/pilotage/en-cours.md`](../docs/pilotage/en-cours.md) est
mise à jour avec : la commande validée (`--rope --val <dir>`, 2,7856), l'interdiction de `--rope`
sans canal (40,0658), l'invariant **3,09** (`v2 : 3,09 tenu`) et le lien vers cette fiche. La ligne
**N — le natif** du tableau des chantiers pointe aussi vers la v2. Les compteurs passent de
**735 / 828** à **736 / 829** (une fiche, un JSON).

## 6. Ce qui pourrait rendre ce rapport faux

- **Une seule graine, un seul run, une seule machine.** 2,7856 vient de `propre512-8k` (graine 1) ;
  pas de barre d'erreur. Le test (2,8566) est la mesure honnête, pas 2,7856.
- **La sélection sur la validation** : 1 024 est le meilleur des quatre points, choisi après coup.
  Le manque réel de la porte est **0,3566** en test, pas 0,2856.
- **`--canal-dir` n'est pas dans le dépôt** : la validation de la forme B repose sur la copie
  `/tmp/eval_n2_propre_rope.py` (v1). Si cette copie disparaît, la commande B n'est plus rejouable
  telle quelle ; la commande A, elle, l'est.
- **Le mètre `eval_longueurs.py` est CUDA-only** et vit dans `work/` (gitignoré) : un clone neuf ne
  peut pas le rejouer. Le sha256 du `.pt` est donné pour la reproductibilité locale.
- **Le contrôle négatif 1 692,39 est un chiffre v1** (à 1 024) ; le 1 673,42 est mesuré à 128 avec
  le correctif patché. Les deux montrent la sensibilité à l'ordre, pas une valeur de porte.
- **Le témoin 3,09 n'est pas le même modèle que la porte** : `A-propre-g1.pt` (11,8 M, absolu, sans
  canal) contre `propre512-8k.pt` (34,3 M, RoPE, canal). C'est voulu : il teste le **mètre**, pas
  une performance comparable.
- **PPL n'est pas lecture** : la porte mesure une perplexité, pas la restitution (règle du miroir).
  Un 2,79 sous 2,5 ne prouverait pas que le modèle lit.

## 7. Fichiers

- **Cette fiche** : `reports/rapport-coordination-n2-v2.md` ; **version machine** :
  [`rapport-coordination-n2-v2.json`](rapport-coordination-n2-v2.json).
- **Lus, non modifiés** : `work/n2ac/eval_longueurs.py`, `work/n2ac/rope_model.py`,
  `work/n2j/evalue_canal.py`, `tools/eval_n2_propre.py`, `tools/native_model.py`,
  `work/n2ac/propre512-8k.pt` (+ `.pt.json`), `work/n2h/A-propre-g1.pt`,
  `data/corpus_propre/{val,test}.{txt,canal}`. **`tools/n2/` n'existe pas dans cet arbre** ;
  aucun fichier de `work/n2ac/` n'a été touché.
- **Copie de travail** : `/tmp/eval_n2_propre_rope.py` (v1, patch `--rope --canal-dir`) ;
  `/tmp/c1-propre-test/` (split de test).
- **Références** : [`rapport-coordination-n2.md`](rapport-coordination-n2.md) (v1),
  [`rapport-etat-n2.md`](rapport-etat-n2.md), [`rapport-n2-porte-propre.md`](rapport-n2-porte-propre.md),
  [`n2-porte-propre.json`](n2-porte-propre.json).
- **Compteurs** : cette fiche ajoute **1 fiche** et **1 JSON** ; `en-cours` passe à **736 / 829**.
- **Aucun commit de N2.** La fiche ne remplace ni `en-cours` ni la roadmap ; elle propose le test,
  elle ne l'écrit pas.
