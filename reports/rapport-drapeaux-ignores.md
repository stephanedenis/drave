# Drapeaux et variables « analysés mais jamais appliqués » — audit systématique
> **Addendum (mêmes jour, après l'audit).** Les défauts n°1 (top-k non transportés
> ni appliqués dans les modes flux), n°2 (`--keep` en `--ppl`), n°3 (`--ffn-gain`
> en `--infer`) et la moitié basse du tableau (`--threads` en FS/PR/BM, `--hebb-q`,
> `--hebb-out`, `--plan` sans `--ctx`, précédence de fenêtre, pas de 2 du mode par
> défaut) ont été **corrigés** dans les commits `7522289` et le suivant. Le
> protocole de flux est passé en **version 4** (puis 5, avec le mode « lot en
> listes ») : le contrat d'activation transporte
> désormais aussi les sept top-k par projection, `--attn-topk`, `--qk-topk` et
> `--moe-topk`. Les sections ci-dessous décrivent l'état AVANT correction — elles
> restent la référence de ce qui a été trouvé, et la liste de ce qui reste
> (`--banc-vision` sans `Options`, `--bits` du noyau GPU, etc.).
>
> **Addendum 2 (même jour, 15h).** La recommandation principale de ce rapport est
> FAITE : `--options-actives` existe et imprime, APRÈS toutes les affectations, les
> réglages que le moteur utilise vraiment (niveaux, seuil, top-k par projection,
> fenêtre, lot, cache KV avec sa variante). Sa première version s'exécutait trop tôt
> en perplexité — elle montrait l'état d'avant les affectations, exactement ce
> qu'elle est censée démasquer — et c'est la relecture adversariale qui l'a pris.
> La variante `--options-strict` n'existe pas ; en revanche un drapeau INCONNU est
> désormais signalé (`--keeep`, `-keep`), ce qui couvre le cas le plus fréquent.


**Révision auditée** : `drave-core/src/main.rs` sha256 `1726f9ac3665c3ce…` (2 999 lignes),
`drave-core/src/model.rs` sha256 `1d7eacc506db6cab…` (3 675 lignes), 30/09 11:54.
Le dépôt était en cours d'édition pendant l'audit (zone flux / préremplissage réparti) :
les numéros de ligne cités sont ceux de cette révision, et **les chemins audités† sont hors
des hunks modifiés** (`git diff` ne touche que la zone ≥ l. 1 240). † mode par défaut,
`--infer`, `--ppl`, `--plan`, boucle d'analyse.

**Périmètre** : 84 drapeaux `--xxx` extraits de `analyser()` (main.rs:396-519) et 26 variables
`DRAVE_*` (27 chaînes, dont le préfixe cité dans un message). Pour chacun : recherche du **site
d'application réelle** (`mdl.champ = …`, argument de `Model::load(…)`, `std::env::var`),
puis de tous les modes qui ne le lisent pas.

**Convention de lecture.** I = `--infer` · P = `--ppl`/`--ppl-texte` · PL = `--plan` ·
T = `--tokenize` · FS = `--flux-serveur` · PR = `--ppl-reparti` · BK = `--banc-kv` ·
BM = `--banc-mla` · GB = `--gpu-banc` · BV = `--banc-vision` · TE = `--tensors` ·
D = mode par défaut (aucun drapeau de mode).
« *sans objet* » = le mode ne fait pas ce que le drapeau règle (ex. `--temp` en perplexité) :
ce n'est **pas** compté comme un défaut. « ignoré » = le drapeau devrait s'appliquer et ne
change rien, en silence.

**Gravité** : 🔴 silencieux **et** change les chiffres (perplexité, jetons, divergence entre
nœuds) · 🟠 silencieux, fausse une mesure, un temps ou une trace · 🟡 sans conséquence notable.

---

## 1. Mode de sélection, sources et génération

| Drapeaux | Appliqué dans (fichier:ligne) | Ignoré / inerte (preuve) | Gravité |
|---|---|---|---|
| `--infer` `--ppl` `--ppl-texte` `--plan` `--tokenize` `--gpu-banc` `--banc-kv` `--banc-mla` `--tensors` `--banc-vision` `--flux-serveur` `--ppl-reparti` | Aiguillage main.rs:47-57 | Si plusieurs sont donnés, **le premier de l'ordre d'aiguillage gagne en silence** (`--ppl f --tensors` fait `--tensors`) | 🟡 |
| `--banc-vision` (le mode) | main.rs:47 appelle `run_banc_vision(&f)` dont la signature est `fn run_banc_vision(sortie: &str)` (main.rs:857) | **Aucune `Options` n'entre dans ce mode** : `--threads`, `--ctx`, `--dense`, `--limit`, `--abits`, `--patch`… y sont tous ignorés. Seuls le chemin du modèle et `DRAVE_VISION_TEXTE` (main.rs:1170) agissent | 🟠 |
| `--ids` | I (main.rs:536, 630) · PR (1683) · BM (1840) | **P** : `run_ppl` ne lit que `ids_file` (2681-2690) ; `--ppl f --ids 1,2,3` ignore `--ids` | 🟡 |
| `--ids-file` | I (630) · P (2640→2681) | PL/T/FS/PR/BK/BM/GB/BV/TE/D : *sans objet* | — |
| `--prompt` | I (580) | P : *sans objet* (P prend un fichier d'identifiants) | — |
| `--texte` `--fichier` `--sortie` | T uniquement (2320-2322) | Ailleurs : *sans objet* | — |
| `--limit` | P (2690) · PR (1669) · GB (2111) | **FS, BM, BV, BK** : jamais lu. En I c'est `--n` qui compte (*sans objet*) | 🟠 |
| `--depuis` | P (2690, 2731, fenêtrage 2794-2806) | Ailleurs : *sans objet* | — |
| `--n` `--temp` `--top-p` `--rep-penalty` `--hist` `--flux` `--session` `--chat` | I (700, 749) | Ailleurs : *sans objet*. **Mais dans I**, le chemin `--topk K>0` (main.rs:712-732) est un argmax glouton : `--temp`, `--top-p`, `--rep-penalty`, `--hist` et `--flux` y sont ignorés sans le dire | 🟡 |

## 2. Moteur, quantification, mémoire

| Drapeaux | Appliqué dans (fichier:ligne) | Ignoré / inerte (preuve) | Gravité |
|---|---|---|---|
| `--keep` | I seulement : `Model::load(…, keep, …)` (550) | **P : `Model::load(…, 1.0, …)` en dur (2707)** · FS (1575) · PR (1675) · BM (1835) · BV (1172). Vérifié empiriquement (§7.1) | 🔴 |
| `--q4` `--q4-ffn` `--q4-attn` `--q4-tout` `--bits-attn` `--bits-ffn` | I (550) · P (2707) · BM : `--dense` seul (1835) | **FS (1575) et PR (1675)** passent `dense=true, auto=false, q4=0, b6=0` en dur : `--q4 --ppl-reparti` mesure un modèle non quantifié en 4 bits | 🔴 |
| `--auto` `--push` | I (550) · P (2707) | FS/PR : `auto=false` en dur (1575, 1675) → `--push` (qui règle aussi `dense=false`) sans effet | 🟠 |
| `--dense` | I (550) · P (2707) · BM (1835) | FS/PR : sans effet car `dense=true` y est déjà forcé — pas de perte, mais le drapeau n'est pas lu ; BV : ignoré ; BK : *sans objet* (le banc KV ne charge pas le modèle) | 🟡 |
| `--threads` | I (548) · P (2678) · BK (1937) · GB (2047) | **FS (1575), PR (1675), BM (1835), BV (1172) : `16` en dur** · **D : avalé par la boucle `i += 2`** (main.rs:65-73, §7.4) | 🟠 |
| `--ctx` | I (547) · P (2677) · FS (1574) · PR (1668) · PL (2444) | **BM (1835 : `4096` en dur)** · **BV (1172 : `512` en dur)** · et en **PL le défaut 512 masque le contexte déclaré** (§7.3) | 🟠 |
| `--abits` | I (549→551) · P (2679→2740) · FS (1576→1216) · PR (1676→1216) | BM/BV : jamais appliqué (`act_levels` reste au défaut 127 = 8 bits, model.rs:1538) | 🟡 |
| `--lot` | I (555→`generate`, model.rs:3505) · P (2867) · **PR (1674, nouveau)** | FS, BM, BV, BK, GB, PL, D : jamais lu. En I, ignoré aussi par le chemin `--topk` (712-732) | 🟠 |
| `--pin` | **Global** : analyser 516 → `engine::EPINGLER` lu par `Pool::new` (engine.rs:388) | Aucun : agit dans tous les modes qui créent un `Pool` (donc dès qu'un modèle est chargé). Inerte en PL/TE (pas de pool) | ✅ |
| `--bits N` | **Global** : analyser 517 → `list::BITS_POIDS` lu par `DenseQ8::dot_q8_source` (list.rs:456) | Appliqué partout où un modèle est chargé… **mais pas par les noyaux GPU** (`gpu.rs` ne cite jamais `BITS_POIDS`) : `--gpu-banc --bits 4` compare un CPU arrondi à un GPU non arrondi, l'écart mesuré est un artefact | 🟠 |

## 3. Attention, rotation, MoE, parcimonie

| Drapeaux | Appliqué dans (fichier:ligne) | Ignoré / inerte (preuve) | Gravité |
|---|---|---|---|
| `--topk-q` `--topk-k` `--topk-v` `--topk-o` `--topk-gate` `--topk-up` `--topk-down` | I (557) · P (2755) | **FS et PR** : `appliquer_quantification` (1214-1220) ne pose que niveaux/seuil/top-k/renorm ; **et l'en-tête de flux ne transporte que ces quatre champs** (`Act` 1265-1270, écriture 1412-1415 et 1442-1445, `TAILLE_TETE` 1261). Les deux nœuds divergent donc **en silence** — exactement ce que le commentaire 1250-1256 dit vouloir empêcher | 🔴🔴 |
| `--moe-topk` | I (552) · P (2739) | FS/PR : jamais lu. Inerte sur modèle dense (model.rs:2417 et 3083 : lu seulement si `n_expert > 0`) | 🔴 (MoE) |
| `--attn-topk` `--qk-topk` | I (564-565) · P (2756-2757) | FS/PR : ni appliqués ni transportés (mêmes preuves que ci-dessus) | 🔴 |
| `--attn-window` | I (559) · P (2759) | FS/PR/BM/BV/BK/GB/PL/D : jamais lu. `--attn-window 0` est de plus ignoré (condition `> 0`) : pour l'annuler il faut `--sans-fenetre` | 🔴 |
| `--sans-fenetre` | I (558) · P (2760) | Idem. **Précédence inversée entre I et P** : en I `--attn-window` l'emporte (558-559), en P c'est `--sans-fenetre` (2759-2760). Mêmes deux drapeaux, résultat opposé selon le mode | 🔴 |
| `--swa-pattern` | I (560) · P (2761) | FS/PR/… : jamais lu | 🟠 |
| `--attn-sinks` | I (561) · P (2767) | FS/PR : jamais lu. **Inerte même là où il est appliqué** si aucune fenêtre n'est active : `ns = if lo > 0 { attn_sinks.min(lo) } else { 0 }` (model.rs:2978, 2996) avec `lo > 0` seulement si `fen > 0`. Et `--attn-sinks 0` n'est jamais appliqué (condition `> 0`) alors que le défaut est 4 (model.rs:1546) | 🟠 |
| `--sans-yarn` | I (566) · P (2758) → `cfg_yarn_off` (model.rs:1750) | FS/PR/BM/BV/BK/GB/PL/T/D : jamais appelé. **De plus la trace `[config] rotation` (model.rs:1360-1367) est imprimée pendant `Model::load`, donc AVANT l'application** : avec `--sans-yarn` elle annonce « YaRN ×N » alors que le calcul fait du RoPE simple | 🟠 |
| `--act-thresh` `--act-topk` `--act-renorm` (et `--abits`→niveaux) | I (553-556) · P (2752-2754) · FS (1576→1216-1219) · PR (1676→1216-1219) | Corrigé récemment : ces quatre-là sont bien appliqués dans les modes flux | ✅ |

## 4. Mesure, trace, expériences

| Drapeaux | Appliqué dans (fichier:ligne) | Ignoré / inerte (preuve) | Gravité |
|---|---|---|---|
| `--trace-flux` `--trace-couches` `--flux-forcer` | P : 2709-2720 | **I** (et partout ailleurs) : jamais lu → `--infer --trace-flux f` ne produit aucun fichier, sans message | 🟠 |
| `--ppl-profil` `--logits-bin` | P : 2854, 2837 | I : jamais lu | 🟡 |
| `--profil-neurones` `--neurones-sortie` | P : 2780, 2942-2945 | I : jamais lu (`activer_profil_neurones` et `rapport_neurones` n'apparaissent qu'en P) | 🟡 |
| `--harmony` `--harmony-assistant` `--harmony-user` `--harmony-suite` `--harmony-contexte` | P : 2647, 2797-2799 | I : jamais lu (I a son propre gabarit via `--chat`, 586-613) → `--harmony-suite --infer` ne fait rien | 🟡 |
| `--patch` | I (643) · P (2746) | Ailleurs : *sans objet* | — |
| `--hebbian` | I (648) · P (2774) | Ailleurs : *sans objet* | — |
| `--hebb-q` | I (648) | **P : `Hebb::new(…, 0.1)` en dur (2774)** — la valeur passée est ignorée | 🟠 |
| `--hebb-out` | I (772) | **P : écrit `/tmp/act_log.bin` et `/tmp/loss_log.bin` en dur (2955-2957)** — le chemin demandé est ignoré | 🟡 |
| `--ffn-gain` | P : 2750 | **I : jamais déstructuré** (bloc 535-542) ni appliqué. Vérifié empiriquement (§7.2) | 🔴 |
| `--matrix` | D (68) · GB (2053-2063) | Ailleurs : *sans objet* (hérité du banc d'origine) | — |
| `--couches-locales` `--flux-liste` `--flux-blocs` | PR seulement (1670, 1677-1679) | Ailleurs : *sans objet* | — |

## 5. Variables d'environnement `DRAVE_*` (26)

| Variable | Appliquée dans (fichier:ligne) | Modes où elle est ignorée / inerte | Gravité |
|---|---|---|---|
| `DRAVE_GPU` | Portail de `gpu::instance()` (gpu.rs:788, 813) | Tous les modes qui ne demandent pas de GPU (PL, T, TE, D, BV, BM) ; les autres variables GPU ne font RIEN sans elle — documenté (REPRISE.md:229) mais silencieux à l'exécution | 🟡 |
| `DRAVE_GPU_TETE` · `DRAVE_GPU_KV` · `DRAVE_GPU_EXPERTS` · `DRAVE_GPU_EXPERTS_GO` | `Model::load` : 1391, 1413, 1505, 1508 | Inutiles sans `DRAVE_GPU` ; sans objet en BK/GB (bancs dédiés) | — |
| `DRAVE_KV_BITS` | `Model::load` (1296) et banc KV (1878) | — | ✅ |
| `DRAVE_KV_F16` · `DRAVE_KV_K_F32` · `DRAVE_KV_V_F32` | `Model::load` (900-903) | — | ✅ |
| `DRAVE_YARN` · `DRAVE_YARN_NON` · `DRAVE_YARN_MSCALE` | `Model::load` (1218-1224) | — (prioritaires sur `--sans-yarn`, qui s'applique après le chargement) | ✅ |
| `DRAVE_YARN_RAMPE` | Chemin RoPE (2049) | — | ✅ |
| `DRAVE_Q8_BLOCS` · `DRAVE_SANS_EMPRUNT` | `DenseQ8::build` (285) · `Proj::load` (345, 352) | — | ✅ |
| `DRAVE_FLUX_VERIF` | Une **seule** occurrence : `forward` jeton par jeton (model.rs:2807) | **Muet dès que `--lot > 1`** : le chemin par lots applique bien le rejeu (`flux_lot`, model.rs:2200 et 2410) mais n'imprime jamais le diagnostic | 🟠 |
| `DRAVE_VISION_TEXTE` | BV seulement (1170) | — | — |
| `DRAVE_HARMONY_TRACE` | `fenetres_harmony` (2606, 2651) | Sans objet hors P + `--harmony` | — |
| `DRAVE_DEBUG_FLUX` | Nœud FS, mode lot (1620) | — | — |
| `DRAVE_BANC_KV_K0` · `_V1` · `_UNIT` · `_GRAD` · `_KUNIT` · `_GPU_SEUL` · `_DEBUG` | BK seulement (1895-2032) | Sans objet ailleurs | — |
| `QT_*` (anciens noms) | Avertissement main.rs:41-44 | **Faux positif** : toute variable d'environnement commençant par `QT_` (ex. `QT_IM_SWITCHER`, présent dans l'environnement de test) déclenche « ancien nom d'une variable : rien n'a été appliqué » | 🟡 |

---

## 6. Ce qui est correct (à ne pas jeter avec le reste)

1. **Les quatre réglages de quantification d'activation** (`--abits`, `--act-thresh`, `--act-topk`,
   `--act-renorm`) sont appliqués **partout** depuis le correctif : I (551-556), P (2740-2754),
   FS (1576→1216), PR (1676→1216). C'est la famille qui a été réparée en dernier, et elle l'est.
2. **Les réglages d'activation voyagent dans le flux** (`Act`, en-tête 1412-1415) : le nœud
   distant applique ceux du client (1585) et non les siens. Le principe est bon — il est
   simplement incomplet (il manque `topk_proj`, `attn_topk`, `qk_topk`, `moe_topk`).
3. `--pin` et `--bits` sont appliqués **globalement dans `analyser`** (516-517) : ils ne peuvent
   pas être oubliés par un mode, seulement être sans objet. C'est le bon modèle à généraliser.
4. `--ppl-texte`, `--depuis`, `--trace-flux` + `--lot` (rejeu et trace passent par `flux_lot`,
   `forward_lot`), `--keep` en I, `--patch` en I/P, `--q4` en I/P : appliqués et vérifiés.
5. La déstructuration par mode (ex. 535-542, 2640-2647) force à **voir** les champs : c'est elle
   qui a fait tomber `--attn-topk`, `--qk-topk` et `--sans-yarn` en inférence. Le `..` final
   reste néanmoins une porte de sortie silencieuse (c'est par elle que `--keep` et `--ffn-gain`
   passent).

## 7. Preuves empiriques (binaire `./drave-core/target/release/drave`, Qwen2.5-0.5B-Q8_0, 4 jetons)

Le binaire date de 11:41 ; les chemins testés ci-dessous n'ont pas été touchés par les
modifications de 11:54 (zone flux ≥ l. 1240). Toutes les commandes sont très courtes
(`--limit 4`, `--n 4`, `--ctx 64`).

**7.1 `--keep` ignoré en `--ppl`, appliqué en `--infer`** 🔴

```
$ drave … --ppl-texte data/wikitext2_test.txt --limit 4 --ctx 64 --threads 4
  === perplexité 1929.3230 sur 3 tokens (0 événements, 0.3 s) ===
$ … + --keep 0.05
  === perplexité 1929.3230 sur 3 tokens (0 événements, 0.3 s) ===   ← identique au chiffre près
$ drave … --infer --ids 1,2,3,4,5 --n 4 --ctx 64 --threads 4
  tokens générés : [6, 25010, 10, 4999]
$ … + --keep 0.05
  tokens générés : [53116, 84925, 36109, 36752]                    ← le drapeau agit bien en I
```
Preuve de code : `run_ppl` passe `1.0` en dur (main.rs:2707) ; `run_infer` passe `keep` (550).

**7.2 `--ffn-gain` ignoré en `--infer`, appliqué en `--ppl`** 🔴

```
$ drave … --ppl-texte … --limit 4 --ctx 64 --threads 4 --ffn-gain 0:4
  gain FFN : couche 0 x 4
  === perplexité 4949.4977 sur 3 tokens … ===                       ← 1929,3 → 4949,5 : appliqué
$ drave … --infer --ids 1,2,3,4,5 --n 4 --ctx 64 --threads 4 --ffn-gain 0:4
  tokens générés : [6, 25010, 10, 4999]                            ← identique sans le drapeau
```
Preuve de code : `ffn_gain` n'est déstructuré que par `run_ppl` (2640-2647) et affecté qu'en
2750 ; `run_infer` ne le mentionne nulle part.

**7.3 `--plan` : le défaut 512 masque le contexte déclaré du modèle** 🟠

```
$ drave models/Qwen2.5-0.5B-Q8_0.gguf --plan
  === contexte : 512 jetons ===
$ drave models/Qwen2.5-0.5B-Q8_0.gguf --plan --ctx 0
  === contexte : 32768 jetons ===
```
Preuve de code : `let ctx_demande = if opt.ctx > 0 { opt.ctx } else { context_length }`
(main.rs:2444-2448), mais `o.ctx` vaut **512 par défaut** (405) : la branche `else`, qui est la
seule documentée par le commentaire, n'est atteignable qu'avec `--ctx 0`.

**7.4 Mode par défaut : la boucle `i += 2` avale `--threads`** 🔴

```
$ drave models/Qwen2.5-0.5B-Q8_0.gguf --threads 4        → threads : 4
$ drave models/Qwen2.5-0.5B-Q8_0.gguf --dense --threads 4 → threads : 30
$ drave … --dense --limit 4 --threads 4                   → threads : 30
```
Preuve de code : main.rs:65-73, `while i < args.len() { match args[i] { … } i += 2; }` — c'est
**exactement** le bug décrit et corrigé dans `analyser` (commentaire 412-418 : « un `i += 2`
global sautait le drapeau suivant après un booléen »). La correction n'a pas été reportée sur
ce chemin.

*Note : toutes les exécutions affichent au passage l'avertissement `QT_IM_SWITCHER … rien n'a
été appliqué`, faux positif de `main.rs:41-44`.*

---

## 8. Recommandation : un tableau de bord `--options-actives`, et trois garde-fous

**L'idée simple** : un drapeau `--options-actives` (et `--options-strict`) qui imprime, au
début de chaque mode, **les réglages réellement en vigueur**, lus sur le modèle *après* toutes
les affectations (`mdl.act_levels`, `mdl.act_thresh`, `mdl.attn_window`, `mdl.keep`…), et qui
signale explicitement chaque drapeau présent dans `argv` mais absent de cette liste :

```
[options] --keep 0.05      : IGNORÉ dans ce mode (--ppl charge toujours le modèle entier)
[options] --threads 4      : inactif (le mode utilise 16 fils en dur)
[options] act_levels=65535  act_thresh=0.05  attn_window=0  moe_topk=0  lot=1  topk_proj=[0;7]
```

Mise en œuvre minimale : une fonction `enregistrer(nom, valeur)` appelée **à chaque site
d'application** (`mdl.act_thresh = opt.act_thresh;` → `appliquer!(mdl, act_thresh)`), plus une
comparaison finale `argv` ↔ registre. `--options-strict` transforme les manquants en erreur.
Trois garde-fous complémentaires, chacun déjà à portée de main :

1. **Supprimer les `..` des déstructurations par mode** (535-542, 2640-2647, …) : le compilateur
   signale alors tout champ jamais lu par le mode. C'est ce qui a fait tomber trois drapeaux ;
   c'est aussi par le `..` que `--ffn-gain` et `--keep` sont passés.
2. **Transporter TOUS les réglages d'activation dans le flux** (`Act` : ajouter `topk_proj`,
   `attn_topk`, `qk_topk`, `moe_topk`) et **incrémenter `VERSION_FLUX`** : le protocole sait déjà
   refuser un pair d'une autre version (1228-1231). Tant que ce n'est pas fait, un nœud peut
   diverger en silence, ce qui est le pire cas de cette famille de bugs.
3. **Un test de non-régression sur la liste des drapeaux** : lire les 84 littéraux de `analyser`
   et exiger que chacun apparaisse dans une table `drapeau → modes où il s'applique` ; tout
   drapeau absent de la table fait échouer le test. Ajouter un test qui lance chaque mode avec
   un drapeau témoin et vérifie que la sortie change (ou est marquée inapplicable).

---

## 9. Résumé

- **110 options auditées** : 84 drapeaux de ligne de commande + 26 variables `DRAVE_*`.
- **46 drapeaux (55 %) sont ignorés dans au moins un mode où ils devraient s'appliquer**,
  dont 20 classés 🔴 (silencieux, et ils changent les chiffres dès que le réglage a un effet
  sur le modèle considéré) ; 5 de plus (`--temp`, `--top-p`, `--rep-penalty`, `--hist`,
  `--flux`) sont ignorés sur le sous-chemin `--topk` de l'inférence. Côté environnement,
  1 variable (`DRAVE_FLUX_VERIF`) est muette dès que `--lot > 1`.
- **Les trois plus graves** :
  1. `--topk-q/-k/-v/-o/-gate/-up/-down` (et `--attn-topk`, `--qk-topk`, `--moe-topk`) ne sont
     ni appliqués ni transportés en `--flux-serveur`/`--ppl-reparti` : deux nœuds peuvent
     diverger **sans aucun message** (main.rs:1214-1220, en-tête 1412-1415).
  2. `--keep` ignoré en `--ppl` : on croit mesurer un modèle élagué, on mesure le modèle entier
     (2707 → `1.0` en dur ; prouvé : 1929.3230 identique à `--keep 0.05` près).
  3. `--ffn-gain` ignoré en `--infer` : la sortie est rigoureusement identique avec et sans le
     drapeau (prouvé : `[6, 25010, 10, 4999]` dans les deux cas).
- Mention spéciale : le **mode par défaut** (aucun drapeau de mode) a gardé la boucle
  `i += 2` (main.rs:65-73) que `analyser` a corrigée — `--dense --threads 4` mesure 30 fils.
