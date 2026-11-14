# N2 — la coordination du mètre : `--rope` ne suffit pas, il faut le canal

> **Ligne de roadmap** : N2 (la porte de perplexité) · **Date** : 2026-11-13 · **HEAD mesuré** :
> `ced21933` · **Verdict** : `tools/eval_n2_propre.py` lit les checkpoints RoPE comme des positions
> absolues et rend **8,0225** sur `propre512-8k` à 128 octets, là où le mètre RoPE rend **2,9726**
> à 128 et **2,7856** à 1 024. Le correctif `--rope` est **nécessaire mais non suffisant** : le
> checkpoint de la porte a été entraîné **avec le canal**, et `--rope` seul rend **40,0658** à 128.
> Le correctif validé est **`--rope --canal-dir`** ; la commande qui donne 2,79 aujourd'hui est le
> mètre existant `work/n2ac/eval_longueurs.py --rope`. **Aucun fichier de N2 modifié**
> (`native_model.py`, `entrainer_native.py`, `work/` intacts).

**En trois lignes.** (1) `charge()` construit `NativeModel` absolu et `ppl_protocole()` oublie le
canal : **deux** causes, pas une. (2) `--rope` seul rend **40,07** ; `--rope --canal-dir` rend
**2,9726** à 128 et **2,7856** à 1 024. (3) La commande qui donne 2,79 aujourd'hui est
`work/n2ac/eval_longueurs.py --rope ... --val data/corpus_propre` (§ 4.A).

## Ce que cette fiche est, et n'est pas

- **Est** : une coordination en lecture seule. Elle rejoue les mesures, isole **deux** causes,
  propose un correctif daté et donne les commandes exactes.
- **N'est pas** : un patch appliqué, un commit, ni une modification de `tools/native_model.py`,
  `tools/entrainer_native.py` ou `work/`. La session N2 reste seule à écrire dans son territoire.
- **Public** : la session N2 (prochaine action : la porte propre, 0,29 manquant à 2,7856).

## 1. Le bug — deux décalages, pas un

### 1.1 L'architecture : `NativeModel` absolu contre `NativeModelRoPE`

`tools/eval_n2_propre.py` construit toujours `NativeModel` :

```python
def charge(chemin, device="cuda"):
    ck = torch.load(chemin, map_location="cpu", weights_only=False)
    cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
                          if k in NativeConfig.__annotations__})
    m = NativeModel(cfg).to(device)          # table de positions apprise absolue
    m.load_state_dict(ck["state"], strict=False)
    m.eval()
    return m
```

Or les checkpoints N2 depuis le 02/11 sont des `NativeModelRoPE`
(`work/n2ac/rope_model.py`) : mêmes noms de tenseurs, **q/k tournés**, `self.pos` hérité mais
**jamais utilisé**. Le chargement est donc **silencieux** :

- 127 clés dans le checkpoint, **0 manquante, 0 inattendue** (`strict=False`) ;
- `pos.weight` est présent dans le checkpoint et chargé dans un modèle qui ne l'a jamais appris ;
- le `NativeModel` absolu l'**applique** à chaque jeton, d'où une PPL qui n'a plus de sens.

Ce n'est pas un `load_state_dict` partiel : c'est un **mauvais choix de classe**, que
`strict=False` ne peut pas signaler puisque les noms de paramètres sont identiques.

### 1.2 Le canal : le second décalage, décisif pour la porte

Le checkpoint de la porte a été entraîné **avec le canal de structure** :

```bash
# work/n2ac/chaine_porte.sh
~/gpu-env/bin/python work/n2ac/entrainer_rope.py \
  --corpus data/corpus_propre/train.txt \
  --canal  data/corpus_propre/train.canal \
  --seq 512 --window 512 --lot 8 --lr 3e-4 --graine 1 \
  --dim 384 --expert-hidden 512 --init work/n2j/base-wiki-45m.pt \
  --pas 8000 --sortie work/n2ac/propre512-8k.pt
```

`ppl_protocole()` de `eval_n2_propre.py` appelle `m(x[:, :-1])` **sans canal**. Sur un modèle
entraîné avec le canal, ce n'est pas une petite différence : c'est une entrée manquante. Mesuré
sur `propre512-8k`, à protocole identique :

| entrée | 128 | 256 | 512 | 1 024 |
|---|---:|---:|---:|---:|
| RoPE, **sans** canal | 40,0658 | 49,5308 | 59,8126 | 65,7898 |
| RoPE, **avec** canal | **2,9726** | **2,8988** | **2,8443** | **2,7856** |

Conséquence : **`--rope` seul déplace le bug, il ne le ferme pas**. Il fait passer le `val` de
8,0225 à 40,0658. Le correctif doit fournir le canal en même temps que la bonne architecture.

### 1.3 Le piège de longueur : 8,02 et 2,79 ne sont pas mesurés à la même longueur

- **8,0225** est le champ `val` de `eval_n2_propre`, mesuré à **128 octets** ;
- **2,7856** est la PPL RoPE + canal à **1 024 octets** ;
- à longueur égale **128**, la référence RoPE + canal est **2,9726**, pas 2,7856.

Le champ `val` de l'outil reste à 128 après le correctif **complet (`--rope --canal-dir`)** : il
vaudra **2,9726**. Le chiffre de la porte est `longueurs["1024"]` = **2,7856**. Il ne faut pas
attendre 2,79 dans `val`.

## 2. Les chiffres

### 2.1 `work/n2ac/propre512-8k.pt` — le checkpoint de la porte

Identité : **34 301 224** paramètres, `window = 512`, `positions = rope`, corpus
`data/corpus_propre/train.txt`, 8 000 pas × 8 × 512, graine 1, sha256 du `.pt`
`37c5673b3d51f6f871c4391b97015b401f73c842d04d4a05f78a70c2b264eefc`.

Courbes de validation sur `data/corpus_propre/val.txt`, au même protocole (fenêtres Van der
Corput dans les chunks de 8 192, 8 lots × 16 fenêtres) :

| mètre | 128 | 256 | 512 | 1 024 |
|---|---:|---:|---:|---:|
| `eval_n2_propre` actuel — absolu, sans canal | 8,0225 | 8,9710 | 11,3357 | 38,5288 |
| `eval_n2_propre --rope` seul — RoPE, sans canal | 40,0658 | 49,5308 | 59,8126 | 65,7898 |
| `eval_n2_propre --rope --canal-dir` — RoPE + canal | **2,9726** | **2,8988** | **2,8443** | **2,7856** |
| référence `eval_longueurs.py --rope` — RoPE + canal | 2,9726 | 2,8988 | 2,8443 | 2,7856 |

Les deux dernières lignes (validation) sont **identiques au chiffre près** : le correctif proposé
reproduit le mètre de référence. Le `1024` de la première ligne est mesuré avec la liste de
longueurs étendue (sans `--rope`, sans canal) ; le `--longueurs` d'origine s'arrête à 512.

Le **test** (split `test.txt` → `val.txt`, `test.canal` → `val.canal`, même mètre RoPE + canal) :

| longueur | test |
|---:|---:|
| 128 | 3,0649 |
| 512 | 2,8875 |
| **1 024** | **2,8566** |
| seuil | 2,5000 |
| manque | **0,3566** |

Le `val` à 1 024 manque la porte de **0,2856** ; le test, mesure honnête, de **0,3566**.

**Contrôles négatifs.**

- **Permutation** : les octets de validation permutés (ordre Van der Corput) donnent
  **1 692,3919** à 1 024 avec le canal inchangé (chiffre publié, reproduit) ; en permutant **aussi
  le canal**, on obtient **1 880,6648**. Les deux valent **600 à 700 fois** 2,7856 : le mètre est
  sensible à l'ordre.
- **Checkpoint absolu `work/n2h/A-propre-g1.pt`** (11 816 136 paramètres, sans canal) :
  `eval_n2_propre` rend **3,0971** en validation et **3,2098** en test, dans la classe des
  3,0904 / 3,1960 publiés. L'outil n'est donc pas cassé pour l'ancienne architecture ; il est
  attaché à elle. Le même checkpoint **avec** canal rend 10,99 : le canal ne s'ajoute pas à un
  modèle qui ne l'a pas appris.

### 2.2 `work/n2ac/rope2048-20k.pt` — le checkpoint le plus récent

Identité : 34 301 224 paramètres, `window = 2048`, `positions = rope`, corpus
`data/wiki_fr/propre/train.txt`, 20 000 pas, `ppl_val` interne 2,4953. Il n'est **pas** le
checkpoint de la porte (corpus différent) ; il sert de second témoin.

| mètre | 128 | 1 024 |
|---|---:|---:|
| `eval_n2_propre` actuel — absolu, sans canal | 12,9098 | — |
| `eval_n2_propre --rope --canal-dir` — RoPE + canal | 5,4773 | 4,6321 |
| référence `eval_longueurs.py --rope` — RoPE + canal | 5,4773 | 4,6321 |

Le **4,63** souvent cité est la valeur à **1 024**, pas à 128. À 128, la référence est **5,4773**.
Ces chiffres sont hors domaine (le modèle a été entraîné sur `data/wiki_fr/propre`) : ils montrent
le bon fonctionnement du mètre, pas une performance de porte.

## 3. Le correctif proposé

### 3.1 `--rope` — le correctif demandé

```diff
-def charge(chemin, device="cuda"):
+def charge(chemin, device="cuda", rope=False):
+    if rope:
+        from work.n2ac.rope_model import charge_rope
+        return charge_rope(chemin, device=device)
     ck = torch.load(chemin, map_location="cpu", weights_only=False)
     cfg = NativeConfig(**{k: v for k, v in ck["config"].items()
                           if k in NativeConfig.__annotations__})
     m = NativeModel(cfg).to(device)
-    m.load_state_dict(ck["state"], strict=False)
+    manquants, inattendus = m.load_state_dict(ck["state"], strict=False)
+    if manquants or inattendus:
+        print(f"  ATTENTION chargement partiel : {len(manquants)} manquants, "
+              f"{len(inattendus)} inattendus", flush=True)
     m.eval()
     return m
```

et, dans `main()` :

```diff
+    ap.add_argument("--rope", action="store_true",
+                    help="checkpoint RoPE (NativeModelRoPE de work/n2ac/rope_model.py)")
...
-    m = charge(a.point, a.device)
+    m = charge(a.point, a.device, rope=a.rope)
```

Le paramètre est optionnel : les importeurs existants (`work/n2h/fenetre.py`,
`work/n2i/typoglycemie.py`, `work/n2k/evalue.py`, `work/n2j/evalue_canal.py`) continuent de
marcher sans changement.

### 3.2 `--canal-dir` — indispensable pour la porte

Le correctif `--rope` seul ne suffit pas (40,0658). Il faut passer le canal aux fenêtres de
validation et de test :

```diff
+def charger_canal(chemin):
+    return torch.tensor(list(pathlib.Path(chemin).read_bytes()), dtype=torch.long)
+
-def fenetres_dans_chunks(data, n, long, compteur, chunk, device="cuda"):
+def fenetres_dans_chunks(data, n, long, compteur, chunk, device="cuda", canal=None):
+    # ... retourne x, ou (x, c) si canal est fourni
-def ppl_protocole(..., device="cuda"):
+def ppl_protocole(..., device="cuda", canal=None):
...
-            logits = m(x[:, :-1])["logits"]
+            logits = m(x[:, :-1], canal=(c[:, :-1] if c is not None else None))["logits"]
```

et dans `main()` :

```diff
+    ap.add_argument("--canal-dir", default=None,
+                    help="répertoire contenant val.canal et test.canal")
...
+    canal_val = (charger_canal(RACINE / a.canal_dir / "val.canal")
+                 if a.canal_dir else None)
+    canal_test = (charger_canal(RACINE / a.canal_dir / "test.canal")
+                  if a.canal_dir else None)
...
-         "val": round(ppl_protocole(m, val, 128, 16, a.chunk, device=a.device), 4),
+         "val": round(ppl_protocole(m, val, 128, 16, a.chunk,
+                                    device=a.device, canal=canal_val), 4),
-         "test": round(ppl_protocole(m, test, 128, 16, a.chunk, 5_000_000,
-                                     device=a.device), 4),
+         "test": round(ppl_protocole(m, test, 128, 16, a.chunk, 5_000_000,
+                                     device=a.device, canal=canal_test), 4),
```

Les autres corpus (`litterature`, `anglais`, `wikitext2`) n'ont pas de `.canal` : ils restent
sans canal, et leurs chiffres ne sont **pas** comparables pour ce checkpoint (voir § 5).
`decompose()` et `ppl_sur_fenetres()` reçoivent le même `canal` ; sans cela, `--decomposition`
mesurerait les têtes précoces sur une entrée incomplète.

### 3.3 `--longueurs` — exposer 1 024

Le chiffre de porte est à 1 024 ; l'option actuelle s'arrête à 512. Remplacer le booléen par une
liste, avec 1 024 dans la valeur par défaut :

```diff
-    ap.add_argument("--longueurs", action="store_true")
+    ap.add_argument("--longueurs", nargs="?", const="129,192,256,384,512,1024",
+                    default=None, metavar="L1,L2,...",
+                    help="longueurs à mesurer (défaut : 129,192,256,384,512,1024)")
...
-        r["longueurs"] = {str(L): round(ppl_protocole(m, val, L, 16, a.chunk,
-                                                      device=a.device), 4)
-                          for L in (129, 192, 256, 384, 512)}
+        r["longueurs"] = {str(L): round(ppl_protocole(m, val, L, 16, a.chunk,
+                                                      device=a.device, canal=canal_val), 4)
+                          for L in (int(x) for x in a.longueurs.split(","))}
```

La commande de la session N2 passe explicitement `--longueurs 128,256,512,1024` pour coller aux
chiffres de référence.

### 3.4 Garde-fou : le sidecar `.pt.json`

Les deux checkpoints RoPE portent `"positions": "rope"` dans leur sidecar. Un garde-fou évite que
le bug se reproduise :

```python
def positions_sidecar(chemin):
    p = pathlib.Path(str(chemin) + ".json")
    if not p.exists():
        return None
    return json.loads(p.read_text()).get("positions")

pos = positions_sidecar(a.point)
if pos == "rope" and not a.rope:
    ap.error(f"{a.point} : sidecar positions=rope ; relancer avec --rope")
if pos == "absolues" and a.rope:
    ap.error(f"{a.point} : sidecar positions=absolues ; retirer --rope")
```

`A-propre-g1.pt` n'a pas de sidecar : le garde-fou ne le bloque pas, et il reste le contrôle
absolu. Le sidecar n'est pas une vérité universelle (les anciens checkpoints n'en ont pas) : c'est
un filet pour les checkpoints N2 récents, pas un remplacement du drapeau explicite.

### 3.5 Le point de durabilité

`--rope` importe `work/n2ac/rope_model.py`, qui est **non suivi** (`work/` est gitignoré). Un
clone neuf ne peut donc pas utiliser le correctif tel quel. Pour rendre le mètre durable, la
session N2 doit, dans l'ordre :

1. **promouvoir** `work/n2ac/rope_model.py` en `tools/rope_model.py` (le module ne dépend que de
   `tools.native_model`) et importer `from tools.rope_model import charge_rope` ;
2. ou intégrer RoPE dans `tools/native_model.py` via un champ de configuration
   (`positions: "absolues" | "rope"`), ce qui est un changement d'architecture plus lourd ;
3. épingler le sha256 du `.pt` et les valeurs de référence dans la future `tools/porte-n2.sh`.

Tant que (1) ou (2) n'est pas fait, le correctif est **local à Hauru**, comme le mètre actuel.

### 3.6 Décision recommandée

**Ne pas livrer `--rope` seul** : il rend 40,07 au lieu de 2,79. Deux chemins propres :

- **(A) `--rope --canal-dir` dans `eval_n2_propre.py`** : le mètre générique devient correct pour
  la porte (val/test) ; l'OOD reste à canalierser par un autre chemin, faute de `.canal` pour ces
  corpus. C'est le plus utile, et c'est celui qui a été validé en copie hors dépôt
  (`/tmp/eval_n2_propre_rope.py`, 2,9726 / 2,8988 / 2,8443 / 2,7856).
- **(B) `--rope` seul dans `eval_n2_propre.py` + `tools/porte-n2.sh`** qui appelle
  `work/n2ac/eval_longueurs.py --rope` pour la porte, et réserve `eval_n2_propre` à l'OOD. C'est
  le plus petit changement, mais il laisse deux mètres pour deux usages.

Dans les deux cas, la commande du § 4.A est la référence qui donne 2,79 aujourd'hui.

## 4. La commande exacte pour la session N2

### A. Aujourd'hui, sans modifier le code — le chiffre 2,79

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python work/n2ac/eval_longueurs.py \
  work/n2ac/propre512-8k.pt \
  --rope --longueurs 128,256,512,1024 --val data/corpus_propre
```

Attendu, à l'identique :

```
L128 : 2.9726
L256 : 2.8988
L512 : 2.8443
L1024 : 2.7856
```

C'est la **seule** commande qui donne 2,79 aujourd'hui ; elle fournit le canal par
`--val data/corpus_propre` (`val.canal`).

### B. Après le correctif `--rope --canal-dir` — la vérification

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python tools/eval_n2_propre.py \
  work/n2ac/propre512-8k.pt \
  --rope --canal-dir data/corpus_propre --longueurs 128,256,512,1024
```

Attendu :

```json
{"fichier": "propre512-8k.pt", "params": 34301224,
 "val": 2.9726, "test": 3.0807,
 "longueurs": {"128": 2.9726, "256": 2.8988, "512": 2.8443, "1024": 2.7856}}
```

Le `test` de cette commande est mesuré à 128 avec l'offset `5_000_000` de l'outil : **3,0807**,
à comparer aux 3,0649 du split de test du mètre RoPE (offset 0) — même classe, pas identique. Le
test de porte à 1 024 reste **2,8566** (commande C).

### C. Le test à 1 024 — la mesure honnête

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
mkdir -p /tmp/propre_test
cp data/corpus_propre/test.txt  /tmp/propre_test/val.txt
cp data/corpus_propre/test.canal /tmp/propre_test/val.canal
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python work/n2ac/eval_longueurs.py \
  work/n2ac/propre512-8k.pt \
  --rope --longueurs 128,512,1024 --val /tmp/propre_test
```

Attendu : **3,0649 / 2,8875 / 2,8566**. Le `val` à 1 024 manque la porte de 0,2856 ; le test de
0,3566.

### D. Le témoin du bug — avant le correctif

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. CUDA_VISIBLE_DEVICES=0 \
  ~/gpu-env/bin/python tools/eval_n2_propre.py \
  work/n2ac/propre512-8k.pt --longueurs
```

Attendu : `"val": 8.0225`, `"test": 8.0126`, et une courbe qui **monte** avec la longueur
(`"129": 8.1024`, `"192": 8.4072`, `"256": 8.9710`, `"384": 10.0906`, `"512": 11.3357`) — le
contraire de la courbe RoPE + canal, qui descend de 2,9726 à 2,7856. C'est le signe que
l'architecture absolue n'a pas de position relative et que le modèle se dégrade quand le contexte
s'allonge.

## 5. Ce qui pourrait rendre ce rapport faux

- **Une seule graine, un seul run, une seule machine.** Les chiffres de la porte viennent de
  `propre512-8k` (graine 1) ; il n'y a pas de barre d'erreur.
- **2,7856 est le meilleur des quatre longueurs en validation**, choisi après coup ; le test
  (2,8566) est la mesure honnête et le manque est 0,3566, pas 0,2856.
- **Le canal n'est pas disponible pour les corpus hors domaine** : les colonnes `litterature`,
  `litterature_propre`, `anglais`, `wikitext2` de `eval_n2_propre` sur ce checkpoint ne sont pas
  comparables. Avec le correctif, elles valent 52,29 / 53,70 / 117,43 / 117,73 (sans canal) ; ce ne
  sont **pas** des mesures de généralisation. Pour l'OOD, il faut calculer le canal du texte
  (`tools/canal_structure.py`) et le fournir, ou passer par un mètre dédié.
- **Le test de `eval_n2_propre` n'est pas le test de la porte** : offset `5_000_000`, longueur
  128, valeur 3,0807. La référence 3,0649 / 2,8566 vient du split `/tmp/propre_test` et du mètre
  `eval_longueurs.py`.
- **`work/` et `data/` sont gitignorés** : la commande est locale à Hauru ; un clone neuf ne peut
  pas la rejouer sans le checkpoint, le corpus et `rope_model.py`. Le sha256 du `.pt` est donné
  ici pour la reproductibilité locale.
- **Le sidecar n'est pas une preuve d'architecture** : `A-propre-g1.pt` n'en a pas ; les anciens
  checkpoints non plus. Le drapeau explicite reste la source de vérité.
- **PPL n'est pas lecture** : la porte mesure une perplexité, pas la restitution (règle du miroir).

## 6. Fichiers

- **Cette fiche** : `reports/rapport-coordination-n2.md` ; **version machine** :
  [`rapport-coordination-n2.json`](rapport-coordination-n2.json).
- **Lus, non modifiés** : `tools/eval_n2_propre.py`, `tools/native_model.py`,
  `work/n2ac/rope_model.py`, `work/n2ac/eval_longueurs.py`, `work/n2j/evalue_canal.py`,
  `work/n2ac/entrainer_rope.py`, `work/n2ac/chaine_porte.sh`,
  `work/n2ac/propre512-8k.pt` (+ `.pt.json`), `work/n2ac/rope2048-20k.pt` (+ `.pt.json`),
  `work/n2h/A-propre-g1.pt`, `data/corpus_propre/{val,test}.{txt,canal}`.
- **Références** : [`rapport-etat-n2`](rapport-etat-n2.md),
  [`rapport-n2-porte-propre`](rapport-n2-porte-propre.md),
  [`n2-porte-propre.json`](n2-porte-propre.json).
- **Fichier neuf, non ajouté à `reports/README.md` ni à `reports/INDEX.md`** (ce serait modifier
  un existant) ; il est découvrable par son nom, comme les autres fiches de coordination.
- **Compteurs** : cette fiche ajoute **1 fiche** et **1 JSON** aux compteurs de `en-cours`
  (au moment de l'écriture : 713 → 714 fiches, 806 → 807 JSON). La session principale les met à
  jour ; cette coordination n'écrit pas `en-cours`.
- **Aucun commit, aucune modification de N2.** La session N2 applique le correctif et commite avec
  le chiffre ; la fiche ne remplace ni `en-cours` ni la roadmap.
