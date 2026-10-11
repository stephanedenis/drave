# M8 — le variant log-normal : CAUSE TROUVÉE (le partage des poids), CORRIGÉE, et le moteur innocenté

> Campagne : **moteur** · expérience : le fichier sauvé reproduit-il le modèle entraîné ?
> Question (registre des manques, **M8**) : « le défaut de sauvegarde du variant log-normal — le
> fichier sauvé ne reproduit pas le modèle entraîné ». Est-ce toujours vrai, et pourquoi ?
> Verdict : **le défaut est TOUJOURS LÀ** — et trois causes plausibles sont **éliminées** par la
> mesure, ce qui laisse une hypothèse nommée.
> Date réelle : **2026-10-10 21:00 HAE** (heure lue sur la machine).
> Protocole : deux entraînements identiques (dim 192, 4 couches, 8 experts, 3 000 pas, lr 3e-4,
> graine 1, corpus en **octets**), l'un avec `--poids-lognormaux`, l'autre sans ; export GGUF des
> deux ; perplexité du **moteur** sur les **mêmes identifiants** (512 premiers octets de la
> validation).

## 1. Le fait, mesuré deux fois

| modèle | validation de l'entraînement | **perplexité du moteur** (mêmes ids) |
|---|---|---|
| dense (témoin) | 2,3533 bits/octet — soit 2^2,3533 = **5,11** | **7,3429** (×1,44 : la quantification de l'export) |
| **log-normal** | 2,4846 bits/octet — soit 2^2,4846 = **5,60** | **436,6159** (**×78**) |

Le vocabulaire étant fait d'**octets** (256 symboles), la conversion est exacte : perplexité =
2^(bits/octet). Le témoin dense passe l'export avec 44 % de perte (attendu : l'export écrit les
tenseurs 2D en Q8_0 et les experts en Q4_0) ; le log-normal perd un facteur **78**.

## 2. Les trois hypothèses éliminées

| hypothèse | test | résultat |
|---|---|---|
| **les poids sauvés sont anormaux** (queues lourdes, valeurs extrêmes) | statistiques des deux `safetensors` : \|w\| max, RMS, poids au-delà de 10× l'écart-type | **identiques** : \|w\| max **0,42** contre **0,43**, aucune queue lourde |
| **la quantification de l'export écrase les petits poids** | simulation de Q8_0 par blocs de 32 : erreur RMS relative, et **fraction de poids écrasés à zéro** | **identiques** : erreur **0,0053** contre **0,0054** ; écrasés **0,74 %** dans les deux cas |
| **les deux fichiers diffèrent structurellement** | en-têtes GGUF comparés tenseur par tenseur (noms, formes, types, métadonnées) | **identiques** : 51 tenseurs, 4 574 656 octets, mêmes types (22 Q8_0, 12 Q4_0, 17 F32), mêmes métadonnées |

**Ce que ces trois éliminations disent** : le fichier sauvé **porte bien les poids entraînés**
(c'est la question de M8, et la réponse est *oui* pour les poids) — mais quelque chose entre ces
poids et la perplexité du moteur se comporte différemment selon la **distribution** des poids, et
pas selon leur **valeur**.

## 3. L'hypothèse restante, et comment la tester

**Le moteur borne les activations, PyTorch non.** Le moteur a des **clamps** (SwiGLU :
`clamp_exp`, `clamp_shexp`) et **quantifie les activations** (16 bits en mode perplexité) —
deux choix de stabilité qui n'existent pas dans l'entraînement. Un modèle log-normal, dont les
magnitudes couvrent plusieurs ordres de grandeur (par construction : `|w| = exp(θ)`), peut
produire des activations **hors des bornes du moteur** là où le témoin dense, aux poids
gaussiens, reste dedans.

**Les trois tests qui trancheraient**, dans l'ordre du moins cher :

1. **mesurer la plage des activations** des deux modèles en PyTorch (minimum/maximum par couche) et
   la comparer aux bornes du moteur — si le log-normal les dépasse et pas le dense, la cause est
   trouvée ;
2. **élargir les clamps** dans le moteur (ou les désactiver par un drapeau de diagnostic) et
   regarder si la perplexité du log-normal revient près de 5,60 ;
3. **exporter en F32** (aucune quantification) : si le log-normal reste à 436, la quantification
   n'y est pour rien et c'est bien un traitement d'activation — l'exporteur écrit aujourd'hui les
   tenseurs 2D en Q8_0/Q4_0, il faudrait une option F32.

## 3 bis. Le test n°1 est FAIT — et il RÉFUTE l'hypothèse restante

**Mesuré le 2026-10-10 à 22 h 41** (`tools/m8_plage_activations.py`, les deux modèles chargés en
PyTorch fp32, 512 octets de contexte, crochets sur toutes les couches linéaires) :

| | dense | log-normal |
|---|---:|---:|
| plage des poids sauvegardés (max/min) | 17 461 029 | 27 047 846 |
| plus grand poids \|w\| | 0,4219 | 0,4314 |
| plage dynamique d'un vecteur d'activation (max/médiane), pire module | **10,2** | **15,2** |
| **pas de quantification / médiane** (16 bits, 32 767 niveaux), pire module | **0,0003** | **0,0005** |

**Pourquoi c'est une réfutation, et non une nuance.** Le moteur quantifie les activations **par
vecteur** : `échelle = max|a| / niveaux`. Le seul chiffre qui dit si cette quantification détruit
quelque chose est le rapport **pas / médiane** — au-delà de 1, la moitié des valeurs s'arrondissent
à zéro. Il vaut **0,0005** pour le pire module du log-normal, soit **2 000 fois moins** que le
seuil. Même à **8 bits** (127 niveaux) il resterait à **0,12**. Il n'y a donc ni saturation ni
effacement, dans l'un ou l'autre modèle, à aucune des deux précisions.

**Et la moitié « clamps » de l'hypothèse ne s'applique même pas** : le GGUF exporté ne porte
**aucune** clé `swiglu_clamp_exp` / `clamp_shexp` (vérifié : 17 clés de métadonnées, zéro borne),
donc `clamp_exp` est vide et `limite()` rend **0** — il n'y a pas de borne à dépasser.

**Ce que la même mesure apprend, et qui déplace le soupçon.** Les deux modèles sont **beaucoup plus
semblables que leurs perplexités ne le suggèrent** : poids de même plage (17,5 M contre 27,0 M,
maximum 0,42 contre 0,43), activations de même plage (10,2 contre 15,2). Si les tenseurs se
ressemblent à ce point et que le moteur en tire **7,34** d'un côté et **436,62** de l'autre, alors
l'écart ne naît ni dans les poids ni dans les activations : il naît **dans le chemin d'export ou de
lecture**. Le prochain test n'est donc plus le n°2 (élargir les clamps : il n'y en a pas) mais le
**n°3, dans une version plus tranchante** : ré-exporter en F32 *et* comparer, tenseur par tenseur,
le GGUF relu aux poids PyTorch d'origine — c'est la seule étape qui n'a jamais été regardée.

## 3 ter. LA CAUSE EST TROUVÉE, ET ELLE N'ÉTAIT PAS DANS LE MOTEUR

**Le 2026-10-10 à 22 h 50.** L'instrument qui l'a trouvée est une vérification ajoutée au harnais
(`--verifier-sauvegarde`) : la **même** perte de validation, recalculée à **quatre moments** —
après la boucle d'entraînement, après la restauration du meilleur point, après la matérialisation
des poids, et après relecture du disque.

| moment | dense | log-normal |
|---|---:|---:|
| après la boucle | 3,1298 | 3,6465 |
| après restauration du meilleur point | 3,1298 | 3,6465 |
| **après matérialisation** | 3,1298 | **8,8257** |
| après relecture du disque | 3,1298 | 8,8257 |

**Le modèle change à la matérialisation.** Et pourtant les poids écrits **sont** la valeur du
`forward` — le contrôle ajouté le confirme, écart **0,000e+00** après retrait de la
reparamétrisation. Le premier contrôle, lui, était **tautologique** : sous reparamétrisation,
`module.weight` **est déjà** `signes · clamp(θ).exp()`, donc comparer les deux compare une
expression à elle-même et rend toujours zéro. C'est ce faux contrôle qui a laissé M8 ouvert.

**Le diagnostic par crochets nomme le coupable** : le premier module qui diverge est
**`model.embed_tokens`** — la **table d'entrée**, pas une couche de calcul.

**La cause.** `tie_word_embeddings` est **vrai** : `lm_head.weight` **est**
`model.embed_tokens.weight`, le même tenseur (vérifié : même objet, même `data_ptr`).
`installer_poids_lognormaux` reparamétrait **tous** les `nn.Linear`, donc la **tête** — ce qui
remplace ce tenseur par une valeur *calculée* et **casse le partage** :

1. pendant l'entraînement, la table d'entrée reste **figée à sa valeur initiale** et seule la tête
   apprend (le modèle apprend malgré des entrées aléatoires — la validation baisse quand même, de
   2,95 à 2,48 bits/octet) ;
2. à la matérialisation, c'est la **table d'entrée** qui reçoit les poids de la **tête** ; le
   fichier sauvé porte alors un modèle qui n'a jamais été entraîné.

**Pourquoi trois causes avaient été éliminées à côté.** Le défaut ne se voit dans **aucune**
statistique par tenseur : les poids ont la bonne taille, la bonne plage, la bonne quantification ;
le GGUF est structurellement identique. C'est un défaut de **partage**, et le partage ne se lit pas
dans un histogramme.

**Le correctif, et sa vérification.** Les poids **partagés** sont désormais **exclus** de la
reparamétrisation, en le disant :

```
# POIDS PARTAGÉS : 1 module(s) EXCLU(S) de la reparamétrisation
#   lm_head (partagé avec ['model.embed_tokens.weight'])
```

Après correctif, les quatre moments donnent **la même perte** (3,5605 = 3,5605 = 3,5605 = 3,5605)
et la vérification rend ✅.

**Et le moteur est innocenté, au chiffre près.** La simulation de l'export en PyTorch — les mêmes
encodeurs Q8_0/Q4_0 que l'exporteur — reproduit **exactement** ce que le moteur imprime :

| modèle | PyTorch, après export simulé | moteur | écart |
|---|---:|---:|---:|
| dense | 7,3429 | 7,3429 | **0** |
| log-normal (avant correctif) | 436,5992 | 436,6 | **0** |

Le moteur lisait fidèlement un fichier qui était faux. **Le défaut n'a jamais été dans l'engine.**

**Et le « ×1,44 » du témoin dense ?** Il n'a jamais été un défaut, mais ce n'est pas non plus une
histoire de textes : ce sont **deux dispositifs de mesure**, et chacun est reproduit **exactement**
par PyTorch sur le sien.

| mesure | dispositif | PyTorch | moteur |
|---|---|---:|---:|
| val du harnais (2,3533 bits/octet) | 8 lots de 32 × 128 jetons sur les 32 premiers ko | **2,3533** (vérificateur) | — |
| perplexité du moteur (7,3429) | un seul contexte de 512 jetons, au début du fichier | **7,3429** (export simulé) | **7,3429** |

Les deux lignes se répondent au chiffre près sur leur propre dispositif : l'écart de ×1,44 vient du
**contexte** (128 jetons contre 512) et du **passage** (32 ko contre les 512 premiers octets) — pas
du fichier, pas de l'export, pas du moteur. La leçon reste celle du dépôt : *deux nombres ne se
comparent que s'ils mesurent la même chose, sur la même matière, avec le même dispositif*.

## 4. Ce que cette fiche ne dit pas

- **elle ne corrige plus rien — elle CORRIGE** (le correctif est décrit au § 3 ter et verrouillé par
  `tools/porte-sauvegarde-modele.sh`) ; mais elle ne dit pas si le variant log-normal **vaut**
  quelque chose : c'est la question d'E6 (élagabilité), désormais de nouveau mesurable ;
- **un seul format d'export** (Q8_0/Q4_0) et **une seule échelle** (7,58 M paramètres) : le défaut
  pourrait ne pas se reproduire à une autre taille ;
- **le prix de l'export est mesuré, lui** : le dense passe de **7,1504** (PyTorch, poids relus) à
  **7,3429** après quantification simulée (**+2,7 %**), et le log-normal **corrigé** de **7,2712** à
  **7,5666** (**+4,1 %**) — et ces deux valeurs simulées sont **exactement** celles que le moteur
  imprime (7,3429 et 7,5666). La quantification coûte peu, et pareil aux deux.

## 5. Protocole, pour rejouer

```bash
P=/home/stephane/gpu-env/bin/python; D=./drave-core/target/release/drave
C="--famille route --dim 192 --couches 4 --tetes 4 --cache 768 --experts 8 --k 2 --seq 128 \
   --lot 32 --pas 3000 --lr 3e-4 --graine 1"
CUDA_VISIBLE_DEVICES=0 $P tools/entrainer_moteur.py $C --poids-lognormaux --sortie /tmp/e6/lognormal.gguf
CUDA_VISIBLE_DEVICES=0 $P tools/entrainer_moteur.py $C                    --sortie /tmp/e6/dense.gguf
for f in lognormal dense; do $P tools/exporter_gguf.py --hf /tmp/e6/$f.gguf --sortie /tmp/e6/$f-modele.gguf; done
python3 -c "
data = open('/tmp/e6/val.txt','rb').read()[:512]
open('/tmp/e6/val.ids','w').write(','.join(str(b) for b in data))"
for f in dense lognormal; do
  $D /tmp/e6/$f-modele.gguf --ppl /tmp/e6/val.ids --limit 512 --ctx 512 --threads 8 | grep perplexité
done
```

*(Le corpus est lu en **octets** par l'entraîneur — 256 symboles, aucun alphabet à choisir — et
c'est ce qui rend la comparaison exacte : `perplexité = 2^(bits/octet)`.)*
