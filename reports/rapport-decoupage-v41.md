# Rapport — Le découpage de V4.1 : la couture exacte, et l'instrument innocenté

02/10 (sprint 13), sur `/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf`
(365,71 Go, 40 couches) et deux nœuds sur la même machine.

**Verdict en une ligne : un V4.1 découpé à la couche 20 rend maintenant le même
état, au bit près, qu'une passe complète à un seul nœud — et l'écart de 7,05e-1
qui l'en empêchait était un vrai défaut du moteur, pas un défaut de l'instrument
qui le mesurait.**

## 1. Les deux questions laissées ouvertes par le sprint 12

| question | réponse |
|---|---|
| pourquoi un V4.1 découpé donnait-il 514 722,06 là où sa propre référence locale donnait 1 743 713,62 ? | la `pre` reçue du pair pour le jeton *p* restait posée sur le modèle et le `forward` du jeton *p+1* la reprenait : le nœud qui commence à la couche 0 amorçait sa chaîne mHC retardée sur les coefficients de la **dernière FFN du pair au jeton précédent** |
| pourquoi la référence locale (1 743 713,62) différait-elle de `--ppl` (208 411,867) sur les mêmes jetons ? | les deux modes ne règlent pas la même quantification d'activation : **16 bits** par défaut en `--ppl` (32 767 niveaux), **8 bits** dans les modes flux (127 niveaux, `appliquer_quantification`) |

## 2. Le défaut de couture, localisé par tenseur

Le harnais `--ppl-reparti` fait deux passes dans le même processus : la référence
locale (modèle entier), puis la passe coupée. Comparer les vides des deux passes
est donc légitime — et c'est ce qui a parlé :

| comparaison (2 544 tenseurs, 40 couches × 4 positions) | tenseurs différents |
|---|---|
| passe répartie **avant** correctif, contre la référence | **629**, tous aux positions **1** (319) et **2** (310), **aucun à la position 0** |
| passe répartie **après** correctif, contre la référence | **0** |
| nœud moteur (couches 20-39, 945 tenseurs), après correctif | **0** |

La position 0 exacte est la signature : au premier jeton il n'y a encore aucune
`pre` reçue, donc rien à fuir. À partir du deuxième, le nœud local héritait des
coefficients du jeton précédent.

## 3. Le correctif, en deux invariants

1. **`Model::forward`** ne consomme la `pre` reçue que si CE nœud **reprend au
   milieu du modèle** (`couche_debut > 0`) : lui seul a besoin d'un chaînon
   précédent pour son premier raccord, qui n'est pas celui du modèle. Un nœud qui
   commence à la couche 0 voit un jeton neuf entrer par l'embarquement ; sa
   chaîne repart de la copie 0, comme la référence.
2. **`Model::norme_finale`** prend `&mut self` et **consomme** cette `pre` : elle
   appartient à la réduction de ce flux-là. La laisser en place, c'était se fier à
   ce que le prochain appel veuille bien ne pas la prendre.

Après correctif, mesuré deux fois (perplexité **et** tenseurs) :

```
  référence locale  : perplexité 1743713.6243  (68.0 s)
  deux nœuds        : perplexité 1743713.6243  (51.3 s)
  écart             : 0.00e0
  transport         : dense f32 · 82016 octets par flux (aller) · 81999 au retour · 3 flux
```

82 016 octets = 79 d'en-tête + 1 de compte `np` + 16 de pré-mix + 20 480 canaux
f32 (4 copies × 5 120). Le pré-mix coûte **0,02 %** du flux et c'est lui qui rend
la couture exacte.

## 4. Pourquoi le V4-Flash ne montrait rien

Sa réduction finale est **apprise** (`output_hc_*`) : il n'a pas de chaîne
retardée, `hc_porte_imposee` n'est jamais posé chez lui et le fil porte `np = 0`.
Le même harnais, le même découpage au même endroit, donnaient déjà **0,00e0** sur
V4-Flash (sprint 12). Un défaut qui ne peut s'exprimer que sur le modèle dont la
réduction finale dépend d'un état transporté — c'est ce qui a rendu l'énigme
longue.

## 5. L'instrument : innocenté, mais à moitié

Le sprint 12 concluait que « l'instrument qui mesure l'écart est suspect ». C'est
**faux**, et la démonstration est directe :

| comparaison | résultat |
|---|---|
| `--ppl --dense` contre `--ppl` | **2 544 tenseurs identiques**, même perplexité (208 411,8674) |
| `--ppl --abits 8` contre la référence du harnais | **2 544 tenseurs identiques**, 1 743 713,6243 |
| `--ppl` (16 bits) contre la référence du harnais (8 bits) | 2 443 tenseurs différents, premier écart `l_last-0-*` = 1,793e-3 |

`--dense` n'est pour rien dans l'affaire. Ce qui diffère, c'est la **quantification
d'activation** : 16 bits en perplexité (la référence de non-régression du dépôt),
8 bits dans les modes flux. Et le premier tenseur qui diverge est `l_last-0-*`, pas
`attn_brut-0-*` — normal : **l'attention V4 est calculée en f32** (`matvec_f32`),
non quantifiée, tandis que le **MoE** l'est. L'attention de la couche 0 est
identique au bit près entre 127 et 32 767 niveaux ; c'est le FFN qui bouge le
premier.

Conséquence pour les chiffres déjà publiés : les « écarts » de `--ppl-reparti`
sont valides (les deux passes du harnais partagent leurs réglages), et le 7,05e-1
du sprint 12 en était un vrai. Ce qui était invalide, c'est la comparaison
*entre* modes sans regarder la quantification — et elle n'était écrite nulle part
sans `--options-actives`.

## 6. Corrigé aussi : le préfixe v6 des modes 3 et 4

Le protocole v6 met un octet `np` (compte de pré-mix) en tête de corps, pour
**tous** les modes. Les deux émetteurs de lots ne l'écrivaient pas : le décodeur
du pair lisait le premier octet du premier état comme un compte et tout le corps
était décalé de quatre octets. Un seul encodeur les sert maintenant
(`prefixe_premix`), avec l'invariant manquant — une `pre` appartient à **un** état.

Mesuré, deux nœuds réels sur `models/Qwen2.5-0.5B-Q8_0.gguf` (24 jetons, ctx 64,
12 couches locales, `--lot 4`) :

| mode | écart référence/deux nœuds | lecture |
|---|---|---|
| 3 — lot dense f32 | **0,00e0** | exact, comme attendu |
| 4 — lot en listes | 4,45e-3 | avec perte, comme son codec |
| 2 — un jeton en listes (comparaison) | 3,65e-2 | le mode 4 est **plus précis** que le mode 2 sur ce modèle |

## 7. Reproduire

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
cargo build --release --manifest-path drave-core/Cargo.toml
D=./drave-core/target/release/drave
M=/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf

# la couture (≈ 4 min : deux chargements de 365,7 Go)
$D "$M" --flux-serveur 47161 --ctx 8 --threads 20 &
$D "$M" --ppl-reparti 127.0.0.1:47161 --couches-locales 20 --limit 4 --ctx 8 \
   --ids "$(cat /tmp/v41_texte.txt.ids)" --threads 20
# attendu : écart 0.00e0, 82016 octets à l'aller, 81999 au retour

# la quantification d'activation, qui explique l'écart entre modes
$D "$M" --ppl /tmp/v41_last4.ids --ctx 8 --limit 4 --threads 20              # 208411.8674 (16 bits)
$D "$M" --ppl /tmp/v41_last4.ids --ctx 8 --limit 4 --threads 20 --abits 8   # 1743713.6243 (= harnais)

# les modes de lot, sur un modèle qui tient en mémoire
$D models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 47181 --ctx 64 --threads 8 &
$D models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:47181 --couches-locales 12 \
   --limit 24 --ctx 64 --lot 4 --threads 8                                   # écart 0.00e0
```

Le digeste tenseur par tenseur de ces comparaisons est versionné :
[`decoupage-v41-digest.txt`](decoupage-v41-digest.txt) (2544 + 945 tenseurs après
correctif, **somme des écarts max = 0,000e+00**).

## 8. Ce qui reste ouvert

- **Un test sur V4.1 lui-même** : la porte rapide
  ([`tools/porte-flux.sh`](../tools/porte-flux.sh), désormais branchée dans
  `portes.sh`) attrape la *classe* de défaut en 20 s sur 0,5 B, mais aucun test
  automatique ne rejoue les 365 Go. Une passe reste une décision manuelle.
- Le **masque des jetons d'image** de l'engram reste un no-op (texte seul).
- Le **régime YaRN au-delà de ~1 024 positions** sur les couches compressées : le
  choix de convention est tranché (YaRN ×16 partout, comme llama.cpp et vLLM), la
  mesure à contexte long reste à faire (`reports/rapport-v4-yarn-compresse.md`).
