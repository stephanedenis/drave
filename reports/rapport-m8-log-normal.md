# M8 — le variant log-normal : trois causes ÉLIMINÉES, une restante nommée

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

## 4. Ce que cette fiche ne dit pas

- **elle ne corrige rien** : M8 reste ouvert, avec une cause nommée au lieu de « cause ouverte » ;
- **un seul format d'export** (Q8_0/Q4_0) et **une seule échelle** (7,58 M paramètres) : le défaut
  pourrait ne pas se reproduire à une autre taille ;
- **le témoin dense n'est pas parfait non plus** (×1,44) : une partie de l'écart appartient à
  l'export, et la part exacte du log-normal dans cet écart n'est pas séparée ici.

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
