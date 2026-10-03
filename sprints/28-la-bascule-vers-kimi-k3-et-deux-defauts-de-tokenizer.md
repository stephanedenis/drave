# Sprint 28 — La bascule : Kimi-K3, deux défauts de tokenizer, et la référence

- **Début** : 09:40 · **Fin** : 11:40
- **Objectif** : sur directive explicite, sortir les modèles périmés du chemin
  critique et travailler sur **les meilleurs modèles ouverts**, « surtout ceux qui
  sont typiquement trop gros pour l'exécution locale ». Ce sprint installe la
  cible (Kimi-K3, 1 508,7 Go en Q4), la **référence exécutable**, et vérifie tout
  ce qui peut l'être **avant** la fin du téléchargement.
- **Engagement de fin** : dépôt vert, machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. La cible, mesurée avant de s'engager

| fait | valeur |
|---|---|
| GGUF | `unsloth/Kimi-K3-GGUF` UD-Q4_K_XL : **1 508,7 Go**, 32 shards, ~110 Mo/s → ~4 h |
| architecture | **`kimi-k3`** : 93 couches, 896 experts dont **16 par jeton**, 1 M de contexte |
| texte | = **Kimi-Linear** : hybride **KDA delta-net** (3 couches sur 4) + **MLA** (`il % 4 == 3`), MoE **latent** (3 584), **attention résiduelle**, **SiTU** |
| cadence **vérifiée sur le fichier** | MLA aux couches **3, 7, 11, 15** (encodé par `attention.head_count_kv = 1` sur ces couches, 0 ailleurs) ; couche 0 dense ; **2 `res_score` sur toutes les couches** |
| **poids par jeton** | **≈ 35 Go** (2,3 % du modèle) → NVMe 17 s/jeton, disque dur 173 s |

### 2. La référence exécutable existe — et elle est construite

llama.cpp **amont** connaît `kimi-k3` (`LLM_ARCH_KIMI_K3`, `src/models/kimi-k3.cpp`),
là où il refuse `deepseek41`. Une **seconde copie** a été clonée et construite
(`llama.cpp-k3`, 6 min) et `tools/ref_logits_k3` est lié contre elle : **la porte
de correction est possible sur cette classe**, ce qui n'était pas le cas pour
V4.1. C'est la première fois qu'un modèle « trop gros pour le local » a les deux
portes disponibles en même temps.

### 3. Le moteur répond AVANT la fin du téléchargement

`--config` et `--tokenize` refusaient un modèle découpé incomplet (« 32 shards
annoncés, 6 présents ») : il fallait attendre la fin d'un transfert de plusieurs
heures pour seulement savoir ce que le fichier contient. Ils acceptent désormais
un modèle partiel **en le disant** (`⚠️ MODÈLE INCOMPLET : 6 shards sur 32`), et
`--config` annonce la liste exacte des manques :

> `calculable : NON — attention delta-net (KDA) : conv1d de 4, porte bornée (−5),
> récurrence par tête · attention résiduelle : pile de points de contrôle tous les
> 12 · MoE latent : projections down/up (latent 3 584) · activation SiTU ·
> redémarrage du flux résiduel aux couches « banque »`

### 4. Deux défauts **silencieux** de tokenizer, trouvés et corrigés

C'est le livrable le plus important du sprint, et il ne coûte rien : la référence
officielle du tokenizer est en Python (le `pat_str` de Moonshot + `tiktoken.model`),
donc vérifiable **sans les poids**.

1. **Le motif `kimi` n'était pas implémenté** : notre tokenizer retombait sur
   qwen2 pour tout ce qui n'est ni qwen2 ni gpt-4o — donc pour
   `tokenizer.ggml.pre = kimi-k2`, que déclarent **Kimi-K2.7 (déjà dans le
   dépôt) et Kimi-K3**. Mesuré : « 2026 » sortait en **un** jeton au lieu de
   « 202 » + « 6 », et le chinois divergeait. Motif transcrit de la référence :
   Han, casse **hors Han**, nombres par trois, contractions en suffixe.
2. **Le découpage par casse enjambait les majuscules** : « HelloWorld » sortait
   d'**un seul morceau** au lieu de « Hello » puis « World ». Ce défaut **ne se
   voyait pas dans les identifiants** (pas de fusion « oW » dans la table, donc
   le résultat tombait juste par chance) — trouvé par un **test unitaire**, puis
   confirmé contre le motif officiel. Corrigé pour les deux matchers (kimi **et**
   gpt-4o).

**État** : 11 textes sur 11 identiques à l'implémentation officielle (français
accentué, anglais, code, chiffres, chinois, casse alternée, espaces) ;
**69 tests unitaires** verts (5 neufs) ; les 512 identifiants gpt-oss de la
référence publiée sont **inchangés** (non-régression mesurée). La porte est dans
le dépôt : `tools/porte-tokenizer-kimi.sh` + `tools/tokenizer_kimi/`.

### 5. La spécification d'architecture, et ce qu'elle change pour nous

`docs/architecture-kimi-k3.md` : inventaire des tenseurs (mesuré), boucle de
couche, `res_mix` (formule exacte : scores sur les valeurs **normalisées**, somme
sur les **brutes**), KDA (conv1d 4, porte bornée), MLA (absorption, `nope`, porte
de sortie), MoE latent (**le routeur note la pleine largeur**), SiTU, et le
`res_mix` final avant la tête. **Ce que nous avons déjà** : MLA, RoPE, MoE,
formats (Q8_0, MXFP4) — acquis. **Ce qui est neuf** : KDA, attention résiduelle,
MoE latent, SiTU, redémarrage du flux. Le nouveau **flux de coupure** (la pile de
points de contrôle, ≤ 8 × 7 168 valeurs) est le sujet de mesure à venir.

### 6. Portes, toutes vertes — et allégées

`tools/portes.sh rapide` : **69 tests** (5 neufs sur le motif kimi), Qwen 19,3885,
clusters 799,8557, quatre routages, engram V4.1 (479 723 rangées), flux relu (51
lignes), rejeu (0 manquante, 0,00e0), porte de correction (71 positions, 100 % des
positions utiles ≥ 0,95), découpage deux nœuds (5 modes). La **perplexité
V4-Flash** — la porte la plus lente (82 Go sur disque dur) — passe derrière
`ARCHIVE=1` : un modèle retiré ne doit pas ralentir les portes vivantes.

**Et une leçon d'outillage payée comptant** : deux commandes de ce sprint se sont
tuées elles-mêmes — `pkill -f portes.sh` et `pgrep -f "bash tools/portes"`
correspondent à la ligne de commande du shell qui les exécute. Le dépôt le disait
déjà pour `pkill -f drave` ; il faut la forme `pkill -x drave` ou l'astuce
`portes[.]sh`. Deux fois plutôt qu'une, donc ça mérite d'être écrit.

## Rétrospective — garder / changer / doute

**Garder.** Vérifier la **référence** avant le modèle. Les deux défauts de
tokenizer ont été trouvés sans une seule once de poids : la référence officielle
est du code, et le vocabulaire vit dans le shard 1. C'est la meilleure heure et
demie du sprint.

**Garder (2).** Le test unitaire qui a trouvé ce que la comparaison d'identifiants
ne pouvait pas voir : « HelloWorld » donnait les BONS identifiants avec un
découpage FAUX. Un test qui vérifie le résultat ne remplace pas un test qui
vérifie l'invariant.

**Changer.** Le refus d'un modèle incomplet était juste dans l'esprit (« un shard
manquant est une erreur, pas un silence ») mais trop grossier dans la lettre : il
empêchait toute inspection pendant un transfert de 4 h. La bonne forme est
« refuser d'exécuter, **accepter d'inspecter**, et dire lequel des deux on fait ».

**Changer (2).** La liste des motifs de tokenizer était un `if/else` à deux
branches avec un repli silencieux sur qwen2. Un repli silencieux sur un motif
inconnu **change les identifiants sans le dire** — exactement ce que le mandat
interdit. À terme : refuser un `pre` inconnu plutôt que de retomber sur qwen2.

**Doute.** Les 35 Go de poids par jeton supposent que **rien n'est réutilisé**
entre jetons. La réutilisation mesurée sur un autre modèle (31,9 % entre jetons
consécutifs) pourrait changer l'ordre de grandeur — mais elle a été mesurée
ailleurs, pas ici. Elle se mesurera sur **ce** modèle, avec la trace de routage,
et c'est le jalon M6.

**Doute (2).** Le disque : 1,5 To de modèle sur un volume de 11 To qui en a 3,4
de libres, plus 341 Go de V4.1-Flash déjà présents. C'est tenable, mais la marge
se réduit si une deuxième cible arrive — et `tools/telecharger_modeles.py` s'arrête
à 300 Go libres, ce qui est la bonne garde.
