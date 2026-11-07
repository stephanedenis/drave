# N2 — l'état du chantier et de sa porte : inventaire, vérification, proposition

> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-06 · **Verdict** :
> N2 n'a **pas** de porte unique dans la passe : sa rouge est une **mesure** — **2,7856** de PPL
> sur le corpus propre à 1 024 octets contre la porte **< 2,5**, soit **0,29** en validation
> (**0,36** en test). Le mètre est **reproductible** (2,7856 / 2,8566 à l'identique, contrôle
> permuté **1 692,39**, deux exécutions égales) et tient en **12 s** de GPU. `tools/eval_n2_propre.py`
> **tourne** sur le checkpoint le plus récent mais **ne le mesure pas** : il charge l'architecture à
> positions **absolues** et rend **12,91** (pire que l'uniforme, 5,55) là où le mètre RoPE rend
> **4,63** ; sur le checkpoint de la porte, **8,02** contre **2,97** à 128 octets. Une
> `tools/porte-n2.sh` est **proposable** : non-régression **≤ 2,80** par défaut, seuil **2,5** en
> mode chantier, **~30–40 s** de GPU, dépendante de `work/` et `data/` **non suivis**.

## La question

Trois choses à établir, sans code : (1) **ce qui existe** — checkpoints, runs documentés, et où
vit la « porte propre » ; (2) **ce que vaut `tools/eval_n2_propre.py`** sur le checkpoint le plus
récent, et ce qu'il mesure vraiment ; (3) **ce que devrait faire** une `tools/porte-n2.sh`, seuil
et coût compris. Les mesures de cette fiche ont été prises à `HEAD = bfd98892` (l'arbre a bougé
pendant l'audit : `d31aa9a2` au départ), le **06/11 entre 21 h 25 et 21 h 41**, GPU libre, une
seule graine, aucune réentraînement.

## 1. Inventaire — les checkpoints

**123 checkpoints `.pt` sous `work/`, 9,52 Go, tous gitignorés** (`work/` l'est ; `data/` aussi) ;
**67** ont un sidecar `.pt.json` (config, corpus, pas, graine, `ppl_val`, durée, sha256 du
`.drvm`). Un 124e `.pt` vit sous `data/adaptateurs/` (tête d'adaptateur, pas N2). Les familles :

| répertoire | taille | ce qu'il porte |
|---|---:|---|
| `work/n2ac/` | **7,7 Go** | la campagne N2 : RoPE, fenêtres, capacité, distillation, porte propre |
| `work/n2j/` | 2,8 Go | bases 34,3 M et canal, avant la fenêtre |
| `work/n2k/` | 1,9 Go | bases multilingue et anglais |
| `work/n2h/` | 1,5 Go | la chaîne honnête N2.h (positions absolues) |
| `work/n2w/` | 1,3 Go | corpus élargi (wiki_big, 60 k pas) |
| `work/n2d/`, `work/n2i/` | 633 Mo, 316 Mo | les premières bases et le corpus élargi |

Les checkpoints qui comptent pour N2, avec leur **date**, leur **taille**, leurs **paramètres**,
leur **recette** et leur `ppl_val` **interne** (contexte d'entraînement — pas la PPL de la porte) :

| rôle | checkpoint | date | MiB | params | recette | `ppl_val` |
|---|---|---|---:|---:|---|---:|
| N2.ac, production 1 Go | `work/n2ac/mix-60k.pt` | 02/11 13:23 | 130,89 | 34,30 M | 60 k × 128 | 3,3556 |
| 200 000 pas | `work/n2ac/mix-200k.pt` | 02/11 19:33 | 130,89 | 34,30 M | 200 k × 128 | 2,9801 |
| fenêtre 512 (61,4 Mo) | `work/n2ac/mix512-15k.pt` | 02/11 20:54 | 130,89 | 34,30 M | 15 k × 512 | 2,7312 |
| fenêtre 1 024 (61,4 Mo) | `work/n2ac/mix1024-7.5k.pt` | 02/11 21:50 | 130,89 | 34,30 M | 7,5 k × 1 024 | 2,6579 |
| production 1 024, 30 k | `work/n2ac/mix1024-30k.pt` | 03/11 02:45 | 130,89 | 34,30 M | 30 k × 1 024 | 2,4828 |
| production 1 024, 60 k | `work/n2ac/mix1024-60k.pt` | 03/11 17:22 | 130,89 | 34,30 M | 60 k × 1 024 | 2,4038 |
| **porte propre — val** | **`work/n2ac/propre512-8k.pt`** | **03/11 02:01** | **130,89** | **34,30 M** | **8 k × 512, init wiki** | **3,3639** |
| porte — bras court | `work/n2ac/propre128-32k.pt` | 03/11 02:33 | 130,89 | 34,30 M | 32 k × 128, init wiki | 3,4500 |
| capacité 11,47 M | `work/n2ac/propre-1147m-512z.pt` | 03/11 13:49 | 45,12 | 11,82 M | 8 k × 512, aléatoire | 3,3650 |
| capacité 21,65 M | `work/n2ac/propre-2165m-512z.pt` | 03/11 14:10 | 82,62 | 21,65 M | 8 k × 512, aléatoire | 3,4394 |
| capacité 34,30 M | `work/n2ac/propre-3430m-512z.pt` | 03/11 14:35 | 130,89 | 34,30 M | 8 k × 512, aléatoire | 3,4682 |
| **le plus récent** | **`work/n2ac/rope2048-20k.pt`** | **04/11 21:09** | **130,89** | **34,30 M** | **20 k × 2 048, init 10 k** | **2,4953** |

Le **checkpoint de la porte** est `propre512-8k.pt` : 137 248 474 octets, sha256
`37c5673b3d51f6f871c4391b97015b401f73c842d04d4a05f78a70c2b264eefc`, config `d_model = 384`,
`n_blocks = 6`, `window = 512`, `early_blocks = (1, 3, 5)`, init `work/n2j/base-wiki-45m.pt`,
8 000 pas × 8 × 512, lr 3e-4, graine 1, perte finale 0,8525, **26 min** de GPU. Le plus récent
(`rope2048-20k.pt`) est un modèle du **grand corpus** (`data/wiki_fr/propre/train.txt`, 186 Mo),
pas du corpus propre : c'est un checkpoint de la fenêtre R1.2, pas de la porte N2.

## 2. Les runs documentés

**40 fiches `reports/rapport-n2-*.md`** couvrent la campagne, du budget (31/10) à la porte
(03/11) : `N2.h1` (corpus propre), `h2` (diversité), `h3` (longueur), `h4` (les deux leviers),
`h5` (capacité), `i` (corpus élargi), `j`–`j4` (corpus réel, positions, capacité, distillation),
`k`–`q` (multilingue et capacité), `r`–`z` (34,3 M, anglais, canal, distillation), `aa`–`ae`
(831 Mo, pas vs texte, mélange, 200 k), `r11`, `fenetre`, `fenetre-r1`, `r12-2048`,
`production-fenetre`, `porte-propre`, `distillation-native`. Soit **une fiche par campagne**, pas
une fiche par checkpoint : **67 / 123** checkpoints ont des métadonnées, et le lien
checkpoint → fiche est **manuel** (les sections « Fichiers » des fiches).

Les correspondances utiles :

| checkpoint | fiche |
|---|---|
| `propre512-8k.pt`, `propre128-32k.pt`, `propre-*-512z.pt` | [`rapport-n2-porte-propre`](rapport-n2-porte-propre.md) |
| `mix-60k.pt` | [`rapport-n2-melange`](rapport-n2-melange.md) |
| `mix-200k.pt` | [`rapport-n2-200k`](rapport-n2-200k.md) |
| `mix1024-30k.pt`, `mix512-15k.pt`, `mix1024-7.5k.pt` | [`rapport-n2-production-fenetre`](rapport-n2-production-fenetre.md) |
| `rope2048-20k.pt` | [`rapport-n2-r12-2048`](rapport-n2-r12-2048.md) (voir la contradiction ci-dessous) |
| `A-propre-g1.pt` (N2.h) | [`rapport-n2-propre`](rapport-n2-propre.md) |

**Une contradiction à corriger dans la fiche R1.2.** La section « Fichiers » de
[`rapport-n2-r12-2048`](rapport-n2-r12-2048.md) (ligne 185) dit : « Le run `rope2048-20k.pt`
**n'a pas été écrit — interrompu** ». Or le fichier **existe** (04/11 21:09, 130,89 MiB, log de
10 000 pas, init `rope2048-10k.pt`, perte finale 0,8965, `ppl_val` 2,4953), et sa mesure au grand
corpus reproduit **exactement** la table de la fiche : **2,9121 / 2,6360 / 2,5375 / 2,4779 /
2,4383** à 128 / 512 / 1 000 / 2 000 / 4 000 octets. C'est donc la **section Fichiers** qui est
périmée (le run a été relancé et fini après la rédaction), pas le chiffre. Le run a coûté
10 220 s (2 h 50).

**A23 confirme le vide outillage** : `tools/porte-n2.sh` **n'existe pas** (l'exemple de la
mission était fictif) ; `eval_n2_propre.py` **exige un checkpoint** positionnel et n'a **pas de
commande unique** ; la tâche T09 de [`rapport-file-taches`](rapport-file-taches.md) est bien
« la porte propre (0,29 manquant à 2,7856) ». Le registre de la dernière passe
(`work/portes-1106-01h28/registre.txt`, 79 vertes / 4 rouges) ne contient **aucune porte N2** :
les 4 rouges sont `bloc-linguistique`, `indice`, `melange`, `sessions`. La « rouge de N2 » n'est
donc **pas** une porte de la passe — c'est le **résultat publié** 2,7856 > 2,5.

## 3. Où est la porte propre

**Le dispositif.** Corpus `data/corpus_propre/` (train 3 244 858 octets, val 180 224, test
180 224 ; 397 / 22 / 22 chunks de 8 192 octets ; **0 % de contamination**, manifeste
[`corpus-propre.json`](corpus-propre.json)), mètre `work/n2ac/eval_longueurs.py --rope` (qui
charge le modèle par `charge_rope`, `work/n2ac/rope_model.py`, et mesure avec
`work/n2j/evalue_canal.py` : 8 lots × 16 fenêtres tirées par Van der Corput **dans** les chunks,
canal fourni, ~131 ko évalués par longueur), checkpoint `work/n2ac/propre512-8k.pt`.

**La commande exacte** (rejouée le 06/11 à 21 h 28) :

```bash
PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 ~/gpu-env/bin/python work/n2ac/eval_longueurs.py \
  work/n2ac/propre512-8k.pt --rope --longueurs 128,256,512,1024 --val data/corpus_propre
```

**Le seuil** est **PPL < 2,5** sur la validation du corpus propre. **Le résultat** :

| longueur | validation | test |
|---:|---:|---:|
| 128 | 2,9726 | 3,0649 |
| 256 | 2,8988 | — |
| 512 | 2,8443 | 2,8875 |
| **1 024** | **2,7856** | **2,8566** |
| **porte** | **2,5** | **2,5** |
| **manque** | **0,2856** | **0,3566** |

Les quatre chiffres de validation et les trois de test sont **identiques au chiffre près** à
[`n2-porte-propre.json`](n2-porte-propre.json) : la mesure est **reproductible**. Le test se
rejoue en reconstruisant le split temporaire que la fiche avait utilisé (`/tmp/propre_test`
n'existe plus) : `test.txt` → `val.txt`, `test.canal` → `val.canal`, puis la même commande avec
`--val /tmp/propre_test` ; vérifié à 21 h 37 (3,0649 / 2,8875 / 2,8566). **Contrôle négatif** :
les mêmes octets de validation **permutés** (ordre Van der Corput), même canal, à 1 024 octets,
donnent **1 692,3919** — le mètre est bien sensible à l'ordre. **Déterminisme** : deux appels
identiques donnent **2,7856** et **2,7856**. **Coût** : 12 s pour les quatre longueurs (chargement
compris), 8 s pour le test, 13 s pour le contrôle.

**Pourquoi 0,29.** 2,7856 − 2,5000 = **0,2856**. Le chiffre est le **meilleur des quatre
longueurs en validation**, obtenu par la recette RoPE + fenêtre 512 + init `base-wiki-45m` ; la
chaîne honnête de N2.h valait **3,0904** (il manquait **0,59**), donc la fenêtre et l'init ont
repris **0,30**. Les leviers déjà fermés :

- **les pas** : le train fait **3,24 Mo**, vu **33 Mo** (≈ 10 époques) ; la validation est
  disjointe par chunks (0 % de fuite), donc allonger le run paierait de la **mémorisation**, pas
  de la donnée — le corpus est **épuisé** ;
- **la capacité** : à 33 Mo vus, 11,47 / 21,65 / 34,30 M donnent **2,8960 / 2,8688 / 2,8662** à
  1 024 octets ; elle **sature** à 21,65 M et laisse encore **0,37** (init aléatoire) ;
- **la distillation** : **rien** à parité stricte (erratum : −0,03 / −0,01 / −0,004 ; le
  +0,14–0,18 était une repondération) ; la paire propre de production vaut −0,06 ;
- **la fenêtre 128** : 3,1107 à 1 024 → la fenêtre large est **nécessaire**, pas suffisante ;
- **la fenêtre 2 048** : à octets constants, elle **ne paie pas** (2,048 derrière 1 024 à 61,4 Mo).

Les leviers restants sont donc **un corpus propre plus large** ou **une distillation à fenêtre
longue** (la note de passage N2 → R1 le demandait déjà) ; ou un **autre corpus de porte** — sur le
grand corpus, la fenêtre 1 024 passe **sous 2,5** (2,4759 / 2,4373 à 1 000 / 2 000 sur la
validation du grand corpus, run 30 k ; 2,3911 / 2,3522 sur la validation du grand corpus, run
60 k — et 2,53 / 2,48 sur la validation française),
mais ce n'est **pas** le corpus propre. Enfin, **0,29 est optimiste** : c'est le meilleur de quatre
longueurs choisi sur la validation ; le **test** donne 2,8566, soit **0,36** de manque.

## 4. `tools/eval_n2_propre.py` sur le checkpoint le plus récent

Le script **tourne** (code 0, 23 s) sur `work/n2ac/rope2048-20k.pt` :

```bash
PYTHONPATH=. CUDA_VISIBLE_DEVICES=1 ~/gpu-env/bin/python tools/eval_n2_propre.py \
  work/n2ac/rope2048-20k.pt --device cuda
```

| checkpoint | architecture | val | test | ce que ça vaut |
|---|---|---:|---:|---|
| `rope2048-20k.pt` (le plus récent) | RoPE | **12,9098** | 12,5881 | **non-sens** : pire que l'uniforme (ln 256 = 5,545) |
| `propre512-8k.pt` (la porte) | RoPE | **8,0225** | 8,0126 | **faux** : le mètre RoPE donne 2,9726 à 128 / 2,7856 à 1 024 |
| `A-propre-g1.pt` (N2.h) | absolue | 3,0971 | 3,2098 | **cohérent** avec 3,0904 / 3,1960 (moyenne de 3 graines) |

**Diagnostic.** `tools/eval_n2_propre.py` charge `NativeModel` (`tools/native_model.py`), qui a une
**table de positions apprises absolue** (`self.pos`) et une attention sans RoPE. Les checkpoints
N2 depuis le 02/11 sont des `NativeModelRoPE` (`work/n2ac/rope_model.py`) : mêmes noms de
paramètres, **q/k tournés**, pas de table utilisée. `load_state_dict(..., strict=False)` charge
donc les 127 tenseurs **sans rien signaler**, et le `pos.weight` du checkpoint (figé depuis
l'init) est appliqué à un modèle qui ne l'a jamais appris : d'où 12,91, pire qu'un modèle
uniforme. Le contrôle sur `A-propre-g1.pt` (absolu) rend 3,0971 / 3,2098, dans la classe des
3,0904 / 3,1960 publiés : **l'outil n'est pas cassé, il est attaché à l'ancienne architecture**.
Trois raisons de plus pour qu'il ne soit pas la porte : il **exige** un checkpoint positionnel,
il n'a **pas** de `--rope`, et ses `--longueurs` s'arrêtent à **512** (129, 192, 256, 384, 512) —
la porte se mesure à **1 024**.

**Conséquence pratique.** La commande que A23 donne pour N2 (`python3 tools/eval_n2_propre.py
<checkpoint>`) appliquée à un checkpoint N2 récent rend **8,02** ou **12,91**, pas **2,79** : elle
ferait conclure à une catastrophe (5 à 10 points de PPL) là où il manque **0,29**. Le correctif
minimal — hors de cette mission, qui est en lecture seule — est un drapeau `--rope` (ou un
auto-diagnostic par le sidecar `.pt.json` : `"positions": "rope"`), plus un avertissement si le
chargement est partiel.

## 5. Proposition — `tools/porte-n2.sh` (sans l'écrire)

**But.** Une porte qui **tourne toujours**, qui **ne peut pas devenir verte sans mesurer**, qui
**n'ajoute pas une rouge permanente par construction**, et qui **imprime le statut absolu** pour
qu'on ne confonde pas « pas de régression » avec « N2 est fini ».

**Ce qu'elle doit mesurer** (une seule charge du modèle, puis les mesures) :

| mesure | comment | attendu (référence) | tolérance |
|---|---|---:|---:|
| identité du checkpoint | params 34 301 224, `window = 512`, sha256 `.pt` `37c5673b…`, sidecar `corpus = data/corpus_propre/train.txt`, `positions = rope` | exact | 0 |
| courbe val 128 / 256 / 512 / 1 024 | `charge_rope` + `evalue_canal.ppl`, `data/corpus_propre/val.*` | 2,9726 / 2,8988 / 2,8443 / **2,7856** | ±0,01 |
| test 1 024 | split temporaire `test.txt` → `val.txt`, `test.canal` → `val.canal` | **2,8566** | ±0,01 |
| forme de la courbe | `PPL(1 024) < PPL(128) − 0,15` (le levier de longueur) | −0,187 | — |
| contrôle négatif | val **permutée** (VDC), même canal, 1 024 | **1 692,39** | > 100 |
| déterminisme | val 1 024 deux fois | 2,7856 = 2,7856 | exact |
| **statut absolu** | `2,7856 − 2,5` | **manque 0,2856** (val), **0,3566** (test) | imprimé |

**Les deux seuils, et pourquoi deux.**

1. **Seuil scientifique : PPL < 2,5** (la porte de la roadmap). Aujourd'hui **rouge**. Il doit
   être **imprimé** à chaque exécution, et **appliqué** seulement en mode chantier
   (`N2_SEUIL=2.5` ou `N2_MODE=porte`), parce qu'une porte rouge **par conception** dans
   `toutes-les-portes.sh` serait une rouge de plus à déclarer dans
   `references-non-regression.md` — et ne distinguerait plus « N2 avance » de « la passe casse ».
2. **Seuil de non-régression (défaut, vert) : PPL_val(1 024) ≤ 2,80** et **PPL_test ≤ 2,87**
   (référence + 0,014 / + 0,013 ; le mètre est déterministe, la marge couvre le changement de
   carte ou de version de torch). Une valeur au-delà est une **régression** du checkpoint ou du
   mètre, pas un progrès de N2.

**Temps.** Mesuré : 12 s (val 4 longueurs), 8 s (test 3 longueurs), 13 s (permutation + double
val), ~2 s (sha256) → **30–40 s** avec une seule charge ; `timeout 300` suffit. La porte complète
coûte ~30 s de plus qu'une passe de 2 h — négligeable. Le mètre actuel est **CUDA-only**
(`evalue_canal.fenetres` fait `.cuda()`) : pas de repli CPU sans un refactor ; si CUDA manque, la
porte doit sortir **2** (artefact ou device absent), jamais 0. Ajouter cette porte à la passe
complète (2 h) coûte **~30 s**.

**Dépendances.** `~/gpu-env/bin/python` (torch 2.11.0+cu130), un GPU, `bash`. Fichiers :
`work/n2ac/eval_longueurs.py`, `work/n2ac/rope_model.py`, `work/n2j/evalue_canal.py`,
`work/n2ac/propre512-8k.pt` (+ `.pt.json`), `data/corpus_propre/{val,test}.{txt,canal}` — **tous
non suivis** (`work/`, `data/` gitignorés) — et `tools/eval_n2_propre.py`, `tools/vdc.py`,
`reports/n2-porte-propre.json` (suivis). Si un artefact manque : **sortie 2** avec le chemin
exact, comme `porte-adaptateur-sortie` ou `porte-budget`.

**Le point dur.** Une porte qui dépend de `work/` et `data/` n'est **pas reproductible sur un
clone neuf** ; c'est déjà le cas de plusieurs portes (elles exigent `models/`), mais pour N2 le
mètre lui-même vit dans `work/` (gitignoré). Pour la rendre durable, il faudrait, hors de cette
mission : **promouvoir** `rope_model.py` et le mètre dans `tools/` (ou ajouter `--rope` à
`eval_n2_propre.py`), **épingler** le sha256 du `.pt` et les valeurs de référence dans la porte,
et garder `reports/n2-porte-propre.json` comme trace suivie. Sans ce déplacement, la porte est
**locale à Hauru** — utile, mais à dire dans son en-tête.

**Ce qu'elle ne doit pas faire.** Réentraîner (8 000 pas = 26 min), télécharger, toucher
`en-cours`/roadmap, mesurer le grand corpus à la place du corpus propre, ni utiliser
`eval_n2_propre.py` **sans** `--rope`. Elle s'appellerait `porte-n2.sh`, serait prise
automatiquement par `toutes-les-portes.sh` (globbing `tools/porte-*.sh`) et ferait passer la
passe de **84 à 85 portes** (le compte de `references-non-regression.md`, 83, est déjà en retard
d'une porte : `porte-produit`).

## 6. Ce qui pourrait rendre ce rapport faux

- **La sélection sur la validation** : 2,7856 est le **meilleur** des quatre longueurs, choisi
  après coup ; le test (2,8566) est la mesure honnête, et il manque **0,36**, pas 0,29.
- **Une seule graine, un seul run, une seule machine** : pas de barre d'erreur sur la porte ; les
  chiffres de capacité viennent de runs à init aléatoire, pas d'une moyenne.
- **Les artefacts sont non suivis** : `work/` et `data/` sont gitignorés ; un clone neuf ne peut
  pas rejouer cette fiche sans le corpus et le checkpoint. Le sha256 du `.pt` est donné ici pour
  la première fois.
- **L'arbre bouge** : `HEAD` est passé de `d31aa9a2` à `bfd98892` pendant l'audit ; les fiches
  citées peuvent avoir changé après 21 h 41. La contradiction R1.2 (`rope2048-20k` « non écrit »)
  en est un exemple.
- **PPL n'est pas lecture** : la porte mesure une perplexité, pas la restitution ; un chiffre sous
  2,5 ne prouverait pas que le modèle lit (règle du miroir).

## 7. Fichiers

- Cette fiche : `reports/rapport-etat-n2.md` ; le condensé machine : `reports/pensee-etat-n2.json`.
- Porte et mesure : [`rapport-n2-porte-propre`](rapport-n2-porte-propre.md),
  [`n2-porte-propre.json`](n2-porte-propre.json), `work/n2ac/chaine_porte.sh`,
  `work/n2ac/eval_longueurs.py`, `work/n2ac/rope_model.py`.
- Production et fenêtre : [`rapport-n2-production-fenetre`](rapport-n2-production-fenetre.md),
  [`rapport-n2-fenetre`](rapport-n2-fenetre.md), [`rapport-n2-r12-2048`](rapport-n2-r12-2048.md).
- Contexte : [`roadmap`](../docs/pilotage/roadmap.md), [`en-cours`](../docs/pilotage/en-cours.md),
  [`file des tâches (A23)`](rapport-file-taches.md), [`eval_n2_propre`](../tools/eval_n2_propre.py).
