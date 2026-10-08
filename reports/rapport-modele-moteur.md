# Le modèle produit ici tourne dans Drave — et se découpe

> 08/10. Deuxième volet de l'objectif : après les bancs (`rapport-parcimonie-entrainee.md`),
> il fallait un modèle **entraîné ici**, **exécuté par le moteur**, et **découpé
> entre deux nœuds**. Les trois sont faits, et chacun a sa porte.
>
> Outils : `tools/entrainer_moteur.py` (entraîne), `tools/exporter_gguf.py`
> (écrit le GGUF), `tools/porte_moteur.py` (fabrique la référence), et
> `tools/porte-reparti-moteur.sh` (la porte de répartition).

---

## 1. La porte d'exécution : tenue

Un Qwen3-MoE entraîné ici (4 couches, 192 cachés, 8 experts, top-2, vocabulaire
d'octets de 256), exporté en GGUF, exécuté par Drave :

| | valeur |
|---|---|
| perplexité, moteur | **5,3397** |
| perplexité, référence PyTorch (mêmes poids quantifiés) | **5,3585** |
| corrélation des logits par position | **min 0,9906** · moyenne > 0,999 |
| accord du top-1 | **95,7 %** |
| `compare_logits.py --porte` | **exit 0** |

Le jumeau dense passe la même porte (corrélation min 0,9998, top-1 98,8 %).

**Ce que la porte exige, et pourquoi.** La référence est construite à partir des
**mêmes poids quantifiés** que ceux du fichier (Q8_0 sur les projections, Q4_0 sur
la FFN et les experts). Comparer le moteur à un modèle en f32 mesurerait la
quantification de l'export, pas le calcul du moteur. C'est la règle du dépôt :
une seconde implémentation de la même formule, pas une seconde exécution de la
même implémentation.

---

## 2. Ce que l'export a coûté à comprendre (trois pièges, tous silencieux)

1. **Les dimensions s'écrivent à l'envers** (ggml range la plus rapide d'abord) ;
   le moteur les remet en convention numpy à la lecture (`gguf.rs`).
2. **Un tenseur d'experts en F32 est REFUSÉ** par le moteur : « format sans noyau
   ni déquantification ». La couche retombe alors sur une FFN dense… qui n'existe
   pas dans un MoE, et le chargement meurt sur `blk.0.ffn_gate.weight absent` —
   un message qui accuse le fichier alors que c'est le format. Les experts sont
   donc écrits en **Q4_0**, et les projections denses en **Q8_0** (`q8_view`
   refuse tout le reste : « type 0 non géré » pour un F32).
3. **`norm_topk_prob` doit être déclaré** (`expert_weights_norm`) : oublié, le
   moteur ne renormalise pas les poids du top-k et le routage change — sans
   qu'aucun tenseur ne manque.

La règle de quantification vit dans **une seule fonction** (`quant_du_tenseur`),
utilisée par l'export *et* par la référence : recopiée des deux côtés, elle avait
divergé (la FFN dense était en Q8_0 dans la référence et en Q4_0 dans le fichier),
et la porte comparait deux quantifications.

---

## 3. La comparaison à lecture égale

Deux modèles de **même lecture par jeton** : `k` experts de 384 valent un FFN
dense de 768, soit **0,59 M poids lus par jeton et par couche** — vérifié dans le
moteur, qui compte **2,3 M paires par jeton** pour les deux.

| | dense | routé |
|---|---:|---:|
| paramètres stockés | 2,26 M | **7,58 M** (×3,35) |
| poids lus par jeton | 2,3 M | 2,3 M |
| **validation, bits/octet** | 2,0903 | **2,0490** |
| **perplexité dans le moteur** | 5,5500 | **5,3397** (−3,8 %) |
| événements par jeton (`--push`) | 2 009 000 | **440 178** (÷4,6) |
| débit moteur (`--push`) | 867 tok/s | **1 222 tok/s** (×1,41) |

**Le routé gagne sur les trois tableaux** : un peu meilleur à lecture égale,
quatre fois moins d'événements, et 1,4× plus rapide dans le chemin par listes.
C'est le régime que l'analyse désignait : beaucoup de paramètres, peu lus.

**Réserve, et elle compte** : les experts sont écrits en **Q4_0**, format pour
lequel le moteur n'a **pas de noyau de listes** — les 1,8 M paires d'experts sont
donc exécutées en dense (le rapport du moteur le dit : « dont en listes : 0,4 M »,
l'attention seule). Les 440 178 événements par jeton sont donc **le plancher** de
ce que le modèle produit : les faire porter par le chemin par listes demande un
noyau Q4_0 en listes, qui n'existe pas.

---

## 4. La porte de répartition : tenue

`tools/porte-reparti-moteur.sh` lance **deux processus** sur le même modèle, deux
plages de couches (2 locales chez le pilote, 2 chez le nœud), et compare à la
perplexité du modèle entier :

```
référence (modèle entier) : 3,9020
deux nœuds                 : 3,9020     écart de flux : 0.00e0
PORTE TENUE : écart relatif 0,0000 %
```

Le transport est exact (f32 dense, 848 octets par flux, 127 flux) et le routage
d'experts ne dépend d'aucun état global : le modèle **se découpe sans changer un
chiffre**.

---

## 5. Deux défauts du moteur trouvés par cette route — et corrigés

1. **`--ppl-reparti` ignorait `--ids-file`** : il ne lisait que `--ids` et
   retombait sur des jetons synthétiques. Deux chemins ne comparaient donc pas les
   mêmes jetons — symptôme : 1 186,53 contre 321,96 de perplexité, attribué au
   découpage alors que l'écart de flux était nul. Corrigé : le fichier est lu.
2. **Ces jetons synthétiques sortaient du vocabulaire** : `1..=limite` demande le
   jeton 256 sur un modèle à 256 entrées → panique à l'indexation des logits, qui
   accuse le modèle. Corrigés : ramenés modulo le vocabulaire.

Portes après correctif : **`cargo test` 77 verts · Qwen 19,3885 · clusters
799,8557 · formats 17/17** — toutes vertes.

---

## 6. Une erreur de mesure à moi, qu'il faut consigner

`entrainer_moteur.py` passait au modèle HF une entrée **déjà décalée** avec des
étiquettes décalées. Or HF décale lui-même (`shift_logits`/`shift_labels`) : le
décalage était appliqué **deux fois**, l'entraînement optimisait la prédiction de
`t+2`, et l'évaluation mesurait ce même objectif décalé. Résultat : des
« 2,95 bits/octet » annoncés pour un modèle qui valait **7,9** — c'est-à-dire
l'uniforme.

Les bancs (`essai_decharge.py`, `essai_blocs.py`) n'ont jamais eu ce défaut : ils
appellent `cross_entropy` eux-mêmes sur des fenêtres décalées une seule fois.
Leur chiffres tiennent. Les chiffres de ce rapport sont postérieurs au correctif.

---

## 7. Réserves

- **Les modèles sont petits** (2,3 M et 7,6 M paramètres) et le corpus fait 100 Mo.
  Rien ici ne dit ce que la comparaison donne à l'échelle ; elle dit que le
  mécanisme fonctionne et que la direction est la bonne à cette échelle.
- **Une seule graine** par configuration.
- **La porte de répartition est tenue sur `127.0.0.1`** : deux processus, une
  machine. Le dépôt a mesuré la latence d'un lien distant
  (`tools/proxy_latence.py` : 1,01× à 0 ms, 1,99× à 5, 4,89× à 20), mais **la
  même expérience sur deux machines n'a pas été faite ici**.
- **Le noyau de listes pour experts Q4_0 n'existe pas** : les 1,8 M paires
  d'experts sont lues en dense. C'est la prochaine marche, et elle est dans le
  moteur, pas dans le modèle.
- Les écarts référence/moteur (0,1 à 0,35 % de perplexité) sont plus grands que
  ceux d'un modèle dense ordinaire : les noyaux Q4_0 du moteur et la
  déquantification de référence ne somment pas dans le même ordre.
